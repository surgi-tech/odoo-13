# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from itertools import zip_longest
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
import logging
_logger = logging.getLogger(__name__)
import logging
import binascii
from struct import unpack
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)


from odoo.addons.rm_bio_attendance.zk import ZK, const


from odoo import api, fields, models
import pytz
import sys
PY3 = sys.version_info >= (3,0)

if PY3:

    xrange = range



def get_time_from_float(float_type):
    str_off_time = str(float_type)
    official_hour = str_off_time.split('.')[0]
    official_minute = (
        "%2d" % int(str(float("0." + str_off_time.split('.')[1]) * 60).split('.')[0])).replace(
        ' ', '0')
    str_off_time = official_hour + ":" + official_minute
    str_off_time = datetime.strptime(str_off_time, "%H:%M").time()
    return str_off_time



def convert_date_to_utc(date, tz):
    local = pytz.timezone(tz)
    date = local.localize(date, is_dst=None)
    date = date.astimezone(pytz.utc)
    date.strftime('%Y-%m-%d: %H:%M:%S')
    return date.replace(tzinfo=None)


def convert_date_to_local(date, tz):
    local = pytz.timezone(tz)
    date = date.replace(tzinfo=pytz.utc)
    date = date.astimezone(local)
    date.strftime('%Y-%m-%d: %H:%M:%S')
    return date.replace(tzinfo=None)


class biometric_record(models.Model):
    _name = 'biometric.record'
    _order = "name desc"

    name=fields.Datetime('Time')
    machine=fields.Many2one('biometric.machine','Machine Name')
    state = fields.Selection([
        ('success', 'Success'),
        ('failed', 'Failed')], default='success', track_visibility='onchange',
        string='Status', required=True, readonly=True, index=True, )
    note=fields.Char('Notes')

class biometric_log(models.Model):
    _name = 'biometric.log'
    _order = "name desc"
    name=fields.Datetime('Time')
    user=fields.Char('User No')
    employee_id=fields.Many2one('hr.employee','Employee')
    machine=fields.Many2one('biometric.machine','Machine Name')
    type= fields.Selection([
        ('in', 'In'),
        ('out', 'Out')], default='in')




class biometric_machine(models.Model):
    _name = 'biometric.machine'

    @api.model
    def _cron_att_download(self):
        print("iam in crone method")
        for mc in self.search([('state', '=', 'active')]):
            mc.download_attendancenew()
        print('i have been finished crone')
        self.download_from_log()

    @api.model
    def _cron_check_connection(self):
        print("iam in crone method")
        for mc in self.search([('state', '=', 'active')]):
            mc.check_notification()




    def check_notification(self):
        for mc in self:
            now = datetime.strftime(datetime.now(), DATETIME_FORMAT)
            yesterday=datetime.strftime(datetime.now()+timedelta(days=-1), DATETIME_FORMAT)
            print('iam in today and yetrerday',now,yesterday)

            records=self.env['biometric.record'].search([('machine','=',mc.id),('name','>=',yesterday),('name','<=',now)])
            print('records is',records,[r.state != 'failed' for r  in records],any([r.state != 'failed' for r in records]))

            if any([r.state != 'failed' for r in records]):
                continue


            if mc.state != 'active':
                continue

            partners = self.env['res.partner']


            for user in self.env['res.users'].search([]):
                if user.has_group('hr_bio_attendance.group_check_bio_attendance'):
                    partners += user.partner_id
            if partners:
                mail_content = _(
                    'Dear Sir, <br> Attendance Biometric Machine:%s Has connection Error Please Check.<br> '
                    'Regards<br>') % (
                               mc.name)
                main_content = {
                 'subject': _('Connection Error For Biometric MAchine Of :%s ') % (mc.name),
                 'author_id': self.env.user.partner_id.id,
                    'body_html': mail_content,
                 'recipient_ids': [(4, pid) for pid in partners.ids],
                }
                self.env['mail.mail'].sudo().create(main_content).send()

    @property
    def min_time(self):
        # Get min time
        if self.interval_min == 'sec':
            min_time = timedelta(seconds=self.time_interval_min)
        elif self.interval_min == 'min':
            min_time = timedelta(minutes=self.time_interval_min)
        elif self.interval_min == 'hour':
            min_time = timedelta(hours=self.time_interval_min)
        else:
            min_time = timedelta(days=self.time_interval_min)
        return min_time

    @property
    def max_time(self):
        # Get min time
        if self.interval_max == 'sec':
            max_time = timedelta(seconds=self.time_interval_max)
        elif self.interval_max == 'min':
            max_time = timedelta(minutes=self.time_interval_max)
        elif self.interval_max == 'hour':
            max_time = timedelta(hours=self.time_interval_max)
        else:
            max_time = timedelta(days=self.time_interval_max)
        return max_time

    @api.model
    def _tz_get(self):
        return [
            (tz, tz) for tz in
            sorted(
                pytz.all_timezones,
                key=lambda tz: tz if not
                tz.startswith('Etc/') else '_')]

    name = fields.Char('Name')
    ip_address = fields.Char('Ip address')
    type = fields.Selection(string="Machine Type", selection=[('in', 'In Only'), ('out', 'Out Only'), ('inout', 'In/Out') ], required=True, default='inout')
    port = fields.Integer('Port',default=4370)
    sequence = fields.Integer('Sequence')
    timezone = fields.Selection(
        _tz_get, 'Timezone', size=64,
        help='Device timezone',
    )
    log_ids = fields.One2many(comodel_name="biometric.record", inverse_name="machine", string="Log", required=False, )
    time_interval_min = fields.Integer(
        'Min time',
        help='Min allowed time  between two registers',default=1)
    interval_min = fields.Selection(
        [('sec', 'Sec(s)'), ('min', 'Min(s)'),
         ('hour', 'Hour(s)'), ('days', 'Day(s)'), ],
        'Min allowed time', help='Min allowed time between two registers',default='sec' )
    time_interval_max = fields.Integer(
        'Max time',
        help='Max allowed time  between two registers', default=1)
    interval_max = fields.Selection(
        [('sec', 'Sec(s)'), ('min', 'Min(s)'),
         ('hour', 'Hour(s)'), ('days', 'Day(s)'), ],
        'Max allowed time', help='Max allowed time between two registers', default='days')
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'InActive')], default='inactive', track_visibility='onchange',
        string='Status', required=False, index=True, )

    attendance_log_ids = fields.One2many('biometric.log', 'machine',
                                         'Logs')

    att_log_cnt = fields.Integer(compute='_compute_attendance_log_cnt')

    def _compute_attendance_log_cnt(self):
        for machine in self:
            machine.att_log_cnt = len(machine.attendance_log_ids)


    def action_view_attendance_log(self):
        self.ensure_one()
        action = self.env.ref(
            'rm_bio_attendance.action_view_biometric_log').read()[0]
        action['domain'] = [('machine', '=', self.id)]
        return action


    def download_from_log(self):
        print('iam in download from log')
        logs=self.env['biometric.log'].search([])
        atts=[]
        for log in logs.sorted(key=lambda l: l.name):
            atttime=log.name
            print ('log time is',atttime)
            type=0
            if log.type=='in':
                type=0
            if log.type == 'out':
                type = 1
            if log.machine:
                tz_info = log.machine.timezone
                local_atttime = convert_date_to_local(atttime, tz_info)
                record_vals = {'name': datetime.now()}
                att=[log.employee_id.att_user_id,False,local_atttime,type]
                try:
                    log.machine.action_create_atts([att])
                except Exception as e:
                    _logger.info("++++++++++++Exception++++++++++++++++++++++", e)
                    record_vals['state'] = 'failed'
                    record_vals[
                        'note'] = 'Successful Connection But there is error while writing attendances from logs as -->log time:%s  log employee:%s the error is **%s**' % (e,log.name,log.employee_id.name)
                    new_record = self.env['biometric.record'].sudo().create(record_vals)
                    break


    def action_download_from_log(self):
        employee_ids = self.env['hr.employee'].search(
            [('att_user_id', '!=', False), ('att_user_id', '>', 0)])
        for employee in employee_ids:
            employee.convert_log_to_attendance()



    def download_attendancenew(self):
        employee_obj = self.env['hr.employee']
        for machine in self:
            machine_ip = machine.ip_address
            port = machine.port
            res=False
            zk = ZK(machine_ip, int(port), timeout=90,ommit_ping=True)
            record_vals = {'name': datetime.now(),
                           'machine': machine.id}
            try:
                res = zk.connect()
                if res:
                    attendance = res.get_attendance()
                    if attendance:
                        try:
                            self.action_create_log(attendance, machine.id)
                            record_vals['state'] = 'success'
                            record_vals['note'] = 'successful connection and attendance logs have been updated'
                            new_record = self.env['biometric.record'].sudo().create(record_vals)
                        except Exception as e:
                            zk.enableDevice()
                            try:
                                zk.disconnect()
                            except BaseException as exp:
                                _logger.info("++++++++++++Exception++++++++++++++++++++++", exp)

                            record_vals['state'] = 'failed'
                            record_vals[
                                'note'] = 'Successful Connection But there is error while writing attendance logs as the error is **%s**' % e
                            new_record = self.env['biometric.record'].sudo().create(record_vals)

                    else:
                        record_vals['state'] = 'success'
                        record_vals['note'] = 'successful connection but there is no attendance logs'
                        new_record = self.env['biometric.record'].sudo().create(record_vals)
            except Exception as exps:
                _logger.info("++++++++++++Exception++++++++++++++++++++++", exps)
                record_vals['state'] = 'failed'
                record_vals['note'] = 'Failed ,please check the parameters and network connections.'


    def action_create_atts(self, bio_attendances):
        employee_obj = self.env['hr.employee']
        for res in self:
            tz_info = res.timezone
            att_users = []
            users_atts = {}
            if not bio_attendances:
                continue
            bio_attendances.sort(key=lambda b: b[2])

            for att in bio_attendances:
                user_no = att[0]
                employee = employee_obj.search([('att_user_id', '=', user_no)], limit=1)
                att_time = att[2]
                time_utc = convert_date_to_utc(att_time, tz_info)
                att_type = att[3]

                if not employee:
                    employee = employee_obj.create({
                        'name': 'Undefined user ID ' + str(user_no),
                        'att_user_id': user_no
                    })
                min_time = res.min_time
                str_att_time_utc = datetime.strftime(convert_date_to_utc(att_time, tz_info),
                                                     DATETIME_FORMAT)
                emp_prev_atts = self.env['hr.attendance'].search(
                    [('employee_id.id', '=', employee.id), ('check_in', '>=', str_att_time_utc)], order='check_in DESC')
                if emp_prev_atts:
                    continue
                prev_att = self.env['hr.attendance'].search(
                    [('employee_id.id', '=', employee.id), ('check_in', '<', str_att_time_utc)],
                    limit=1, order='check_in DESC', )
                if prev_att and prev_att.check_out:
                    checkout_time = prev_att.check_out
                    if checkout_time >= time_utc:
                        print("i will cintinue because the alste attendance checkout in bigger than current")
                        continue
                elif prev_att and not prev_att.check_out:
                    checkin_time = prev_att.check_in
                    if att_type == 0:
                        if min_time >= (time_utc - checkin_time):
                            # print('iam in the main and there in multi punch ')
                            continue
                if user_no not in att_users:
                    users_atts[user_no] = []
                    att_users.append(user_no)
                users_atts[user_no].append((att_time, att_type))
            for user, atts in users_atts.items():
                employee = employee_obj.search([('att_user_id', '=', user)], limit=1)
                attendances = sorted(atts, key=lambda t: t[0])
                if attendances:
                    for user_att in attendances:
                        res.create_attendance(employee.id, user_att[0], user_att[1])


    def create_attendance(self, emp_id, time, type):
        employee_obj = self.env['hr.employee']
        att_obj = self.env['hr.attendance']
        for res in self:
            tz_info = res.timezone
            if emp_id and time and type in (0,1):
                time_utc = convert_date_to_utc(time, tz_info)
                str_att_time_utc = datetime.strftime(convert_date_to_utc(time, tz_info),
                                                     DATETIME_FORMAT)
                max_time = res.max_time
                min_time = res.min_time
                prev_att = self.env['hr.attendance'].search(
                    [('employee_id.id', '=', emp_id), ('check_in', '<=', str_att_time_utc)],
                    limit=1, order='check_in DESC', )
                if not prev_att:
                    # print('there is no prev atts and i will create new')
                    if type == 0:
                        print('type is check in')
                        new_attendance = att_obj.create({
                            'employee_id': emp_id,
                            'check_in': str_att_time_utc,
                            'state': 'right'
                        })
                    elif type == 1:
                        new_time = time_utc - timedelta(milliseconds=1)
                        str_new_time_utc = datetime.strftime(new_time, DATETIME_FORMAT)
                        new_attendance = att_obj.create({
                            'employee_id': emp_id,
                            'check_in': str_new_time_utc,
                            'check_out': str_att_time_utc,
                            'state': 'fixin'
                        })
                else:
                    if prev_att.check_out:
                        checkout_time = prev_att.check_out
                        if checkout_time >= time_utc:
                            continue
                        if type == 0:
                            new_attendance = att_obj.create({
                                'employee_id': emp_id,
                                'check_in': str_att_time_utc,
                                'state': 'right'
                            })
                        elif type == 1:

                            if checkout_time >= (time_utc - min_time):
                                prev_att.write({
                                    'check_out': str_att_time_utc,
                                })
                            else:
                                new_checkin_time = time_utc - timedelta(milliseconds=1)
                                new_attendance = att_obj.create({
                                    'employee_id': emp_id,
                                    'check_in': datetime.strftime(new_checkin_time, DATETIME_FORMAT),
                                    'check_out': str_att_time_utc,
                                    'state': 'fixin'

                                })
                    else:
                        checkin_time = prev_att.check_in
                        if checkin_time >= time_utc:
                            continue
                        if type == 0:
                            if min_time >= (time_utc - checkin_time):

                                continue
                            str_new_checkout_time = datetime.strftime(checkin_time + timedelta(milliseconds=1),
                                                                      DATETIME_FORMAT)

                            prev_att.write({
                                'check_out': str_new_checkout_time,
                                'state': 'fixout'
                            })
                            new_attendance = att_obj.create({
                                'employee_id': emp_id,
                                'check_in': str_att_time_utc,
                            })
                        elif type == 1:
                            if max_time >= (time_utc - checkin_time):
                                prev_att.write({
                                    'check_out': str_att_time_utc,
                                })
                            else:
                                new_time = time_utc - timedelta(milliseconds=1)
                                str_new_time_utc = datetime.strftime(new_time, DATETIME_FORMAT)

                                str_new_checkout_time = datetime.strftime(checkin_time + timedelta(milliseconds=1),
                                                                          DATETIME_FORMAT)
                                prev_att.write({
                                    'check_out': str_new_checkout_time,
                                    'state': 'fixout'
                                })

                                new_attendance = att_obj.create({
                                    'employee_id': emp_id,
                                    'check_in': str_new_time_utc,
                                    'check_out': str_att_time_utc,
                                    'state': 'fixin'

                                })





    def action_create_log(self, atts,machine_id):
        if  not atts:
            return
        for res in self:
            employee_obj = self.env['hr.employee']
            log_obj = self.env['biometric.log']
            machine=self.env['biometric.machine'].browse(machine_id)
            if not machine:
                continue

            tz_info = res.timezone
            for i, att in enumerate(atts):
                print('the attendance is in new',att)
                user_no = att.user_id
                att_time = att.timestamp
                employee = employee_obj.search([('att_user_id', '=', user_no)], limit=1)
                str_att_time_utc = datetime.strftime(convert_date_to_utc(att_time, tz_info),
                                                         DATETIME_FORMAT)

                prev_log = self.env['biometric.log'].search(
                        [('employee_id', '=', employee.id), ('name', '>=', str_att_time_utc), ('machine', '=', machine_id)],
                        limit=1 )
                if prev_log:
                    continue
                att_type = att.punch
                type_att='in'
                if att_type==1:
                    type_att = 'out'

                new_log=log_obj.sudo().create({
                        'user':user_no,
                        'employee_id':employee.id,
                        'name':str_att_time_utc,
                        'machine': machine_id,
                        'type':type_att if machine.type =='inout' else machine.type
                    })



