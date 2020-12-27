
import time
from odoo import api, fields, models, _



class configure_attendence(models.TransientModel):

    _name = "configure.attendence"


    def _get_interval_number(self):
        line_id = self.env['ir.cron'].search([('name', 'ilike', 'Download Attendance')])
        return line_id.interval_number


    def _get_interval_type(self):
        line_id = self.env['ir.cron'].search([('name', 'ilike', 'Download Attendance')])
        return line_id.interval_type
    
    interval_number = fields.Integer(string="Interval Number" ,default=_get_interval_number, )
    interval_type = fields.Selection([('minutes','Minutes'),('hours','Hours'),('work_days','Work Days'),('days','Days'),('weeks','Weeks'),('months','Months')],string="Interval Unit",default=_get_interval_type)
    




    

    def update_interval(self):
 
        for line in self:
            interval_number = line.interval_number
            interval_type = line.interval_type

        line_id = self.env['ir.cron'].search([('name','ilike','Download Attendance')])
        print (line_id)
        line_id.write({'interval_number': interval_number,'interval_type':interval_type})
