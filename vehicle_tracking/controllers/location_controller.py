from odoo import http
from odoo.http import request, Response
import json


class VehicleCurrentLocation(http.Controller):

    @http.route('/get_vehicle_location', type='http', auth='public', website=True)
    def get_vehicle_location(self):
        vehicle_current_coordinates = request.env['vehicle.location'].sudo().search([],order = 'create_date desc', limit=1)
        coordinates_list = []

        for record in vehicle_current_coordinates:
            coordinates_list.append({
                'latitude': record.latitude,
                'longitude': record.longitude,
                'gpstime': record.gps_time,
                'address': record.address
            })

        response = {
            'status': 'success',
            'data': coordinates_list,
        }
        # print(response)
        return Response(json.dumps(response), content_type='application/json')

    @http.route('/get_initial_coordinates', type='http', auth='public', methods=['GET'])
    def get_coordinates(self, **post):
        # order_id = post.get('order_id')
        sale_order_name = 'S00003'
        sale_order_ref = request.env['sale.order'].sudo().search([('name','=',sale_order_name)])
        sale_order_id = sale_order_ref.id
        print(sale_order_id)
        order_delivery_ref = request.env['stock.picking'].sudo().search([('sale_id', '=', sale_order_id)])
        print(order_delivery_ref)
        vehicle_ref = order_delivery_ref.assigned_vehicle
        ref_vehicle_id = vehicle_ref.id

        # For vehicle longitude and latitude
        vehicle_current_latitude = float(vehicle_ref.current_latitude) or 0.0
        print(vehicle_current_latitude)
        vehicle_current_longitude = float(vehicle_ref.current_longitude) or 0.0
        print(vehicle_current_longitude)

        # For warehouse longitude and latitude
        warehouse_ref = order_delivery_ref.location_id.warehouse_id
        ref_warehouse_id = warehouse_ref.id
        warehouse_latitude = float(warehouse_ref.latitude) or 0.0
        print(warehouse_latitude)
        warehouse_longitude = float(warehouse_ref.longitude) or 0.0
        print(warehouse_longitude)

        # For shipping address latitude and longitude or user address
        destination_partner_address_ref = order_delivery_ref.partner_id
        ref_partner_id = destination_partner_address_ref.id
        destination_location_latitude = float(destination_partner_address_ref.latitude) or 0.0
        print(f"Destination: {destination_location_latitude}")
        destination_location_longitude = float(destination_partner_address_ref.longitude) or 0.0

        delivery_effective_date = order_delivery_ref.date_done
        response = {
            "status": "success",
            "data": {
                'source_location': {
                    'warehouse_id': ref_warehouse_id,
                    'latitude': warehouse_latitude,
                    'longitude': warehouse_longitude
                },
                'destination_location': {
                    'partner_id': ref_partner_id,
                    'latitude': destination_location_latitude,
                    'longitude': destination_location_longitude
                },
                'assigned_vehicle_current_coordinates': {
                    'assigned_vehicle_id': ref_vehicle_id,
                    'latitude': vehicle_current_latitude,
                    'longitude': vehicle_current_longitude
                },
            }
        }
        return Response(json.dumps(response), content_type='application/json')


    @http.route('/update_assigned_vehicle_location', type='http', auth='public', website=True)
    def get_vehicle_location(self,**post):
        # vehicle_id = post.get('vehicle_id')
        vehicle_id = 5
        vehicle_current_coordinates = request.env['driver.current.state.location'].sudo().search([('vehicle_id','=',vehicle_id)],order = 'create_date desc', limit=1)
        print(vehicle_current_coordinates)
        coordinates_list = []


        for record in vehicle_current_coordinates:
            print(record.current_latitude)
            coordinates_list.append({
                'latitude': record.current_latitude,
                'longitude': record.current_longitude,
                # 'time': record.create_date
            })

        response = {
            'status': 'success',
            'data': coordinates_list,
        }
        # print(response)
        return Response(json.dumps(response), content_type='application/json')



