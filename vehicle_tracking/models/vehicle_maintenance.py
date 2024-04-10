# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime,timedelta

class vehicle_maintenance(models.Model):
    _name = 'vehicle.maintenance.log'
    _description = 'vehicle_maintenance.vehicle_maintenance'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    related_driver = fields.Many2one('driver.details', string="Associated Driver")
    last_maintenance_date = fields.Date(string="Last Maintenance Date")
    next_maintenance_date = fields.Date(string="Next Maintenance Date")
    maintenance_cost = fields.Float(string="Maintenance Cost")
    maintenance_vendor = fields.Many2one('res.partner', string="Maintenance Vendor")
    maintenance_notes = fields.Text(string="Maintenance Notes")
    

    # # @api.depends('last_maintenance_date')
    # def maintenance(self):
    #     # Data fetching from vehicle.mileage.log model
    #     vehicle_mileage_ref = self.env['vehicle.mileage.statistics'].search([])
    #     print(vehicle_mileage_ref)
    #     print("red")
        
    #     for rec in vehicle_mileage_ref:
    #         total_mileage = rec.travelled_distance
    #         print(total_mileage)
    #         total_engine_hours = rec.vehicle_engine_hours
    #         print(total_engine_hours)
    #         current_vehicle_id = rec.vehicle_id
    #         threshold_mileage = current_vehicle_id.threshold_mileage
    #         print(threshold_mileage)
    #         threshold_engine_hours = current_vehicle_id.threshold_engine_hours
    #         # threshold_mileage = self.env['fleet.vehicle'].search([('name','=',current_vehicle_name)]).threshold_mileage
    #         if total_mileage >= threshold_mileage or total_engine_hours >= threshold_engine_hours:  
    #             print("Please Sir your vehilce needs an maintenance ")
    #         #     return "Hello"
#     def check_maintenance_activity(self):
#         # Data fetching from vehicle.mileage.log model
#         vehicle_mileage_ref = self.env['vehicle.mileage.statistics'].search([])
#         print(vehicle_mileage_ref)
#         print("red")
        
#         for rec in vehicle_mileage_ref:
#             travelled_distance = rec.travelled_distance
#             print(travelled_distance)
#             total_engine_hours = rec.vehicle_engine_hours
#             print(total_engine_hours)
            
#             # This below is for the mantenance schedular based on the time interval
#             vehicle_id = rec.vehicle_id
#             for rec in vehicle_id:
#                 manufacturer_recommend = rec.manufacturer_recommended_interval
#                 print(manufacturer_recommend)
                
                
#                 regulator_recommend = rec.regulator_recommended_interval
#                 print(regulator_recommend)
                
                
#                 mean_recommend = (manufacturer_recommend+regulator_recommend)/2
#                 print(mean_recommend)
                
                
#                 odometer_value_id = self.env['fleet.vehicle.odometer'].search([('vehicle_id','=',rec.id)],order='date desc',limit=1)
#                 last_service_date = odometer_value_id.date
#                 print(last_service_date)
                
                
#                 today_date = datetime.now().date()
#                 print("Today's date:", today_date)
#                 servicing_needed_date = last_service_date+timedelta(days=mean_recommend)
#                 print(servicing_needed_date)
                
                
#                 current_vehicle_id = rec.id
#                 print(current_vehicle_id)
                
                
#                 threshold_mileage_id=self.env['fleet.vehicle'].search([('id','=',current_vehicle_id)])
#                 threshold_mileage_id_value=threshold_mileage_id.threshold_mileage
#                 print(threshold_mileage_id_value)
                
                
#                 odometer_value_id=self.env['fleet.vehicle.odometer'].search([('vehicle_id','=',current_vehicle_id)], order='date desc', limit=1)
#                 odometer_value_id_value=odometer_value_id.value
#                 print(odometer_value_id_value)
                
                
#                 if today_date >= servicing_needed_date or travelled_distance>= odometer_value_id_value+threshold_mileage_id_value:
#                     print("servicing needed")
                            

#                     if travelled_distance>= odometer_value_id_value+threshold_mileage_id_value:
#                         print(f"Servicing is needed for ur {rec.vehicle_id.name}")
#                         template_ref = self.env.ref('vehicle_tracking.vehicle_maintenance_email_template')
#                         return template_ref.send_mail(self.id, force_send=True)



            
            
            
            
            

#             else:
#                 print("servicing not needed")
        
#         #         vehicle_id = self.env['fleet.vehicle'].search([])
#         # print(vehicle_id)






#         # total_distance_travelled = vehicle_mileage_ref.distance_travelled
#         # engine_hours = vehicle_mileage_ref.vehicle_engine_hours

#         # # Data fetching from vehicle.maintenance.interval model
#         # vehicle_maintenance_interval_ref = self.env['vehicle.maintenance.interval'].search([('vehicle_id','=',self.vehicle_id)], order='date desc', limit=1)
#         # default_maintenance_interval = vehicle_maintenance_interval_ref.default_maintenance_interval
#         # manufacturer_recommended_interval = vehicle_maintenance_interval_ref.manufacturer_recommended_interval
#         # regulator_recommended_interval = vehicle_maintenance_interval_ref.regulator_recommended_interval


# # class VehicleMileage(models.Model):
# #     _name = 'vehicle.milage.log'
# #     _description = "Capturing data related to vehicle Maintenance"

# #     vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
# #     distance_travelled = fields.Float(string="Mileage Till Date")

