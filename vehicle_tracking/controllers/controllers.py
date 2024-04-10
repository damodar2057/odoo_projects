from odoo import http
from odoo.http import request
import json

class LocationController(http.Controller):

    @http.route('/update_location',auth='public',type='http',methods=['POST'],csrf=False,cors='*')
    def update_location(self,**post):   
        latitude = post.get('latitude')
        longitude = post.get('longitude')
        vehicle_id = post.get('vehicle_id')
        vehicle_status = True
        driver_current_location_ref = request.env['driver.current.state.location'].sudo().search([])
        driver_current_location_ref.create({
            'vehicle_id':vehicle_id,
            'current_latitude':latitude,
            'current_longitude':longitude,
            'status': vehicle_status
        })


        print("Helo triggered from flutter")

    # @http.route('/track-order',auth='public',type='http',website=True,cors='*')
    # def render_track_order_page(self):
    #     print("laptop intruder")
    #     print("laptop intruder")
    #     print("laptop intruder")
    #     print("laptop intruder")
    #     print("laptop intruder")
    #     print("laptop intruder")
    #     print("laptop intruder")
    #     print("laptop intruder")
    #     return request.render('vehicle_tracking.track_order_template',{})

    # This shows the form in the website for vehicle request
    @http.route('/vehicle-request-employee',auth='public',type='http', website=True,cors='*')
    def render_vehicle_request_page(self):
        vehicle_list_ref = request.env['fleet.vehicle'].sudo().search([])
        # print(vehicle_list)
        vehicle_list = []
        for rec in vehicle_list_ref:
            vehicle_name= rec.name
            vehicle_list.append(vehicle_name)


        return request.render('vehicle_tracking.vehicle_request_template',{'vehicle_list':vehicle_list})
    
    
    
    @http.route('/submit/vehicle-request-employee',auth='public',type='http',methods=['POST'],csrf=False,website=True)
    def submit_vehicle_request_data(self,**post):
        vehicle_id = post.get('inputVehicle4')
        vehicle_ref = request.env['fleet.vehicle'].sudo().search([('name','=',vehicle_id)])
        print(vehicle_ref)
        requested_by = request.env.user.id
        print(requested_by)
        purpose = post.get('inputPurpose')
        print(purpose)
        requested_duration = post.get('inputRequestedHours')
        use_date = post.get('inputRequestedDate')
        print(use_date)
        start_point = post.get('inputSourceLocation')
        print(start_point)
        destination_point = post.get('inputDestinationLocation')
        print(destination_point)
        
        fleet_request_model_ref = http.request.env['vehicle.request.office.employee'].create({
            'vehicle_id':vehicle_ref.id,
            'requested_by':requested_by,
            'purpose':purpose,
            'requested_duration':requested_duration,    
            'start_point':start_point,
            'destination_point':destination_point,

            
        })
        print(fleet_request_model_ref)

        return request.redirect('/')
    
    # this is for the submission of the fuel consumption details

    @http.route('/fleet-fuel-consumption',auth='public',type='http',website=True,cors='*')
    def render_fuel_consumption_page(self):
        vehicle_list_ref = request.env['fleet.vehicle'].sudo().search([])

        petrol_price = request.env['ir.config_parameter'].sudo().get_param('vehicle_tracking.petrol_price') or 0.0
        diesel_price = request.env['ir.config_parameter'].sudo().get_param('vehicle_tracking.diesel_price') or 0.0
        gasoline_price = request.env['ir.config_parameter'].sudo().get_param('vehicle_tracking.gasoline_price') or 0.0

        print(petrol_price)
        # print(vehicle_list)
        # renewal_alert_period = int(self.env['ir.config_parameter'].sudo().get_param('vehicle_tracking.renewal_alert_period',default=30))
        # print(renewal_alert_period)
        vehicle_list = []
        for rec in vehicle_list_ref:
            vehicle_name= rec.name
            vehicle_list.append(vehicle_name)
        print("Hello damodar from controller")
        return request.render('vehicle_tracking.fuel_submit_template',{'vehicle_list':vehicle_list,'petrol_price':petrol_price,'diesel_price':diesel_price,'gasoline_price':gasoline_price})
    

    @http.route('/submit/fleet-fuel-consumption',auth='public',type='http',methods=['POST'],website=True,csrf=False,cors='*')
    def render_track_order_page(self,**post):
        vehicle_id = post.get('inputVehicle4')
        vehicle_ref = request.env['fleet.vehicle'].sudo().search([('name','=',vehicle_id)])
        print(vehicle_ref.id)
        requested_by = request.env.user.id
        print(requested_by)
        odoometer_reading = post.get('inputOdoometerReading')
        print(odoometer_reading)
        
        driver = post.get('inputDriver4')
        fueling_station = post.get('inputFuelingStation')

        fueling_date = post.get('inputFuelingDate')
        fuel_type = post.get('fuel_type')
        print(fuel_type)
        per_unit_price = post.get('inputFuelRate')
        fuel_quantity = post.get('inputFuelQuantity')

        total_cost = post.get('totalCost')
        payment_method = post.get('payment_method')

        receipt_number = post.get('inputReceiptNumber')
        receipt_document = post.get('inputReceiptDocument')
        
        notes = post.get('notes')
        for record in vehicle_ref:
                
            fuel_consumption_ref = request.env['fuel.consumption'].sudo().create({
                'vehicle_id':record.id,
                'fueling_station':fueling_station,
                'fuel_type':fuel_type,
                'per_unit_price':per_unit_price,
                'fuel_quantity':fuel_quantity,
                'total_cost':total_cost,
                'payment_method':payment_method,
                'receipt_number':receipt_number,
                'receipt_document':receipt_document 
                
                
            })
        
        
        
        print(f"Driver:{driver},odoometer_reading:{odoometer_reading},fueling_station:{fueling_station},fueling_date:{fueling_date},fuel_type:{fuel_type},total_cost:{total_cost},payment_method:{payment_method},receipt_number:{receipt_number},receipt_document:{receipt_document},notes:{notes}")

        return request.render('vehicle_tracking.fuel_submit_template',{})
    

    # @http.route('/fetch/fleet-based/on-status',auth='public',type='http',methods=['GET'])
    # def update_location(self):
    #     latitude = post.get('latitude')
    #     longitude = post.get('longitude')
    #     vehicle_id = post.get('vehicle_id')
    #     vehicle_status = True
    #     driver_current_location_ref = request.env['driver.current.state.location'].sudo().search([])
    #     driver_current_location_ref.create({
    #         'vehicle_id':vehicle_id,
    #         'current_latitude':latitude,
    #         'current_longitude':longitude,
    #         'status': vehicle_status
    #     })


    #     print("Helo triggered from flutter")