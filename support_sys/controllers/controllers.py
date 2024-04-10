from odoo import http
from odoo.http import request
import base64
import json
from datetime import datetime

class TicketController(http.Controller):
    @http.route('/ticket_raise', auth='user', website=True)
    def authenticate_user(self, **kw):
        user=request.env.user.partner_id
        print(user.name)
        ticket = request.env['ticket.type'].sudo().search([])
        ticket_list = []
        for tl in ticket:
            ticket_list.append({
                'id': tl.id,
                'name': tl.name,
            })
        product = request.env['company.service.category'].sudo().search([])
        product_list = []
        for pl in product:
            product_list.append({
                'id': pl.id,
                'name': pl.name,
            })

        return request.render('support_sys.ticket_raise',{'ticket':ticket_list,'product':product_list,'customer':user.name,})

    @http.route('/company_products', auth='user', website=True)
    def company_products(self, **kw):
        user=request.env.user.id
        company_services_ref = request.env['company.services'].sudo().search([])
        return request.render('support_sys.company_products_list_template',{'show':True,
                                'services_list':company_services_ref
                                    })
    @http.route('/company_bank_details', auth='user', website=True)
    def company_bank_details(self, **kw):
        user=request.env.user.id
        bank_list_ref = request.env['company.bank.details'].sudo().search([])
        return request.render('support_sys.company_bank_details_list_template',{'show':True,
                                'bank_list':bank_list_ref
                                    })


    @http.route('/employee_residence', auth='user', website=True)
    def employee_residence(self, **kw):
        user=request.env.user.id
        employee = request.env['hr.employee'].sudo().search([('user_id','=',user)])
        residence_status_ref = request.env['hotel.stay.model'].sudo().search([('employee_id','=',employee.id)])

        return request.render('support_sys.employee_residence_template',{'show':True,
                                'residence_status_info_list':residence_status_ref
                                    })

    @http.route('/residence_status_form', auth='user',csrf=False, website=True)
    def render_residence_status_form(self, **kw):
        photo = request.httprequest.files.get('photoBill')
        photo_read = photo.read() if photo else False
        photo_encode = base64.b64encode(photo_read) if photo_read else False
        
        employee=request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
        if request.httprequest.method == 'POST':
            request.env['hotel.stay.model'].sudo().create({
                'employee_id':employee.id,
                'residence':kw.get('residence'),
                'hotel_name':kw.get('hotelName'),
                'contact_person':kw.get('contactPerson'),
                'contact_number':kw.get('contactNumber'),
                'client_id':kw.get('client'),
                'hotel_detail':kw.get('hotelDetail'),
                'estimated_accomodation_expenditure':kw.get('dailyaccomodationspending'),
                'estimated_meals_expenditure':kw.get('dailymealspending'),
                'supporting_documents':photo_encode,
            })
            # request.redirect('/employee_residence')


        client_ref = request.env['client.info'].sudo().search([])
        client_list = []
        for client in client_ref:
            client_list.append({
                'client_id':client.id,
                'client_name':client.name
                })
        print(client_list)
        return request.render('support_sys.residence_status_form',{'show':True,'clients':client_list})



    @http.route('/submit/ticket_raise', methods=['POST'], csrf=False, auth='user', website=True)
    def new_ticket_raised(self, **post):
        client_id=request.env.user.partner_id.id
        project=post.get('project')
        ticket_type=post.get('ticket-type')
        product_category=post.get('product-category')
        priority=post.get('priority')
        subject=post.get('subject')
        issue=post.get('issue')
        notes=post.get('message')
        proof_document = request.httprequest.files.get('docs')
        if proof_document:
            file_data = proof_document.read()
            file_data_base64 = base64.b64encode(file_data)
        else:
            file_data_base64 = False
        http.request.env['ticket.request'].sudo().create({
            'ticket_type':ticket_type,
            'company_service_category_id':product_category,
            'client_id':client_id,
            'priority':priority,
            'subject':subject,
            'issue':issue,
            'notes':notes,
            'project':project,
            'issue_supporting_document':file_data_base64
        })
        return request.redirect('/ticket_raise')

    @http.route('/expenditure_data', auth='user', website=True)
    def expenditureData(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        employee_ref = request.env['hr.employee'].search(
            [('user_id', '=', request.env.user.id)])
        show=False
        if(employee_ref):
            show=True
        currency = request.env['res.currency'].search([])
        currency_list = []
        for cl in currency:
            currency_list.append({
                'id': cl.id,
                'name': cl.name,
            })
        project=request.env['company.project'].sudo().search([])
        project_list=[]
        for pl in project:
            project_list.append({
                'id':pl.id,
                'name':pl.name,
            })
        client=request.env['client.info'].sudo().search([])
        client_list=[]
        for cl in client:
            client_list.append({
                'id':cl.id,
                'name':cl.name
            })
        branch = request.env['branch.info'].sudo().search([])
        branch_list = []
        for bl in branch:
            branch_list.append({
                'id': bl.id,
                'name':bl.name
            })
        expense = request.env['expense.type'].sudo().search([])
        expense_type = []
        for et in expense:
            expense_type.append({
                'id': et.id,
                'name': et.name
            })
        return request.render("support_sys.expenditure_form", {'employee':employee_ref,'show':show,'currency':currency_list,'project':project_list,'client':client_list,'branch':branch_list,'expense':expense_type,'dept':dept_details})

    @http.route('/submit/expenditure_data', methods=['POST'], csrf=False, auth='user', website=True)
    def expenditure_data_submit(self, **post):
        employee_ref = request.env['hr.employee'].search([('user_id','=',request.env.user.id)])
        currency_id=post.get('currency')
        amount=post.get('amount')
        project=request.httprequest.form.getlist('project')
        print(project)
        client=request.httprequest.form.getlist('client')
        print(client)
        location=post.get('location')
        # start_date=post.get('start-date-bs')
        # end_date=post.get('end-date-bs')
        start_date=post.get('start_date')
        end_date=post.get('end_date')
        # branch=post.get('branch')
        expense=request.httprequest.form.getlist('expense')
        print(expense)
        note=post.get('note')
        expense_description=post.get('expense_description')
        file_upload = request.httprequest.files.get('proof')
        file_data = file_upload.read()
        file_data_base64 = base64.b64encode(file_data)
        data=http.request.env['expense.request'].sudo().create({
        'employee_id':employee_ref.id,
        'serviced_client_id':[(6,0,client)],
        'project_id':[(6,0,project)],
        # 'branch_id':branch,
        'expense_type':[(6,0,expense)],
        'expense_description':expense_description,
        'expense_start_date':start_date,
        'expense_end_date':end_date,
        'currency_id':currency_id,
        'amount':amount,
        'priority':post.get('priority'),
        'starting_location':location,
        'ending_location':location,
        'notes':note,
        'receipt_attachment':file_data_base64
        })
        return request.redirect('/expenditure_data')

    @http.route('/daily_tasks', auth='user', website=True)
    def dailyTasks(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
            

        employee_ref = request.env['hr.employee'].sudo().search(
            [('user_id', '=', request.env.user.id)])
        show = False
        if (employee_ref):
            show = True
        work_list=[]
        for wl in employee_ref.task_type:
            work_list.append({
                'id':wl.id,
                'name':wl.work_type
            })
        task_assignment_ref = request.env['employee.task.assignment'].sudo().search([
            ('employee_id','=',employee_ref.id),
           ('status','=','onprogress' )                                                                   
        ])
        client_list_array =  task_assignment_ref.mapped('client_id')
        
        client_list=[]
        for cl in client_list_array:
            
            client_list.append({
                'id':cl.id,
                'name':cl.client_name,
            })
        print(client_list)
        branch=request.env['branch.info'].sudo().search([])
        branch_list=[]
        for bl in branch:
            branch_list.append({
                'id':bl.id,
                'name':bl.name,
                'client':bl.related_client_id.id
            })
        branch_json = json.dumps(branch_list)
        project_list=[]
        for pl in employee_ref.project:
            project_list.append({
                'id': pl.id,
                'name': pl.name,
            })
        return request.render("support_sys.daily_tasks", {'project':project_list,'branches':branch_json,'client':client_list,'employee':employee_ref,'show':show,'work':work_list,'dept':dept_details})

    @http.route('/submit/daily_tasks',method=['POST'],csrf=False, auth='user', website=True)
    def submitDailyTasks(self, **post):
        employee_ref = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)])
        work_type=post.get('work-type')
        work_date=post.get('date')
        start_time=post.get('start_time')
        end_time=post.get('end_time')
        client=post.get('client')
        branch=post.get('branch')
        project=post.get('project')
        supporting_docs = []
        if 'docs' in request.httprequest.files:
            docs = request.httprequest.files.getlist('docs')

            if docs and any(docs):
                for file in docs:
                    file_data = base64.b64encode(file.read())
                    supporting_docs.append({'file': file_data})

        task_detail=post.get('task_detail')
        note=post.get('note')
        request.env['employee.daily.work.report'].sudo().create({
            'employee_id':employee_ref.id,
            'work_type':work_type,
            'task_detail':task_detail,
            'start_time':start_time,
            'end_time':end_time,
            'additional_notes':note,
            'supporting_docs': [(0, 0, {'name': f'File {i + 1}', 'datas': file_info['file']}) for i, file_info in enumerate(supporting_docs)] or None,
            'work_date':work_date,
            'client_id':client,
            'branch_id':branch or False,
            'project_id':project
        })
        return request.redirect('/daily_tasks')

    @http.route('/advance_request', auth='user', website=True)
    def advance_request_details(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        print("calling advance request")
        employee_ref = request.env['hr.employee'].search(
            [('user_id', '=', request.env.user.id)])
        show = False
        if (employee_ref):
            show = True
        expense = request.env['expense.type'].sudo().search([])
        expense_type = []
        for et in expense:
            expense_type.append({
                'id': et.id,
                'name': et.name
            })
        currency = request.env['res.currency'].sudo().search([])
        currency_list = []
        for cl in currency:
            currency_list.append({
                'id': cl.id,
                'name': cl.name,
            })
        return http.request.render('support_sys.advance_request_template', {'employee':employee_ref,'show':show,'expense':expense_type,'currency':currency_list,'dept':dept_details})

    @http.route('/submit/advance_request',methods=['POST'], csrf=False, auth='user', website=True)
    def advance_request_submit(self, **post):
        employee_ref = request.env['hr.employee'].search(
            [('user_id', '=', request.env.user.id)])
        expense=request.httprequest.form.getlist('expense')
        amount=post.get('advance-amount')
        currency=post.get('currency')
        date_from=post.get('start-date')
        date_to=post.get('end-date')
        docs=request.httprequest.files.get('proof')
        file=docs.read()
        file_upload=base64.b64encode(file)
        reason=post.get('reason')
        note=post.get('note')
        http.request.env['advance.request'].sudo().create({
            'employee_id':employee_ref.id,
            'expense_type':[(6,0,expense)],
            'currency_id':currency,
            'requested_amount':amount,
            'date_from':date_from,
            'date_to':date_to,
            'priority':post.get('priority'),
            'file_upload':file_upload,
            'advance_request_reason':reason,
            'notes':note,
        })
        return request.redirect('/advance_request')

    @http.route('/view_tasks', auth='user', website=True)
    def view_assigned_tasks(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group(
            'employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        employee_ref = request.env['hr.employee'].search(
            [('user_id', '=', request.env.user.id)])
        show = False
        if (employee_ref):
            show = True
            task_assigned=request.env['employee.task.assignment'].sudo().search([('employee_id','=',employee_ref.id),('status','=','onprogress'),])
            task_list=[]
            i=0
            for ta in task_assigned:
                i=i+1
                task_list.append({
                    's_no':i,
                    'id':ta.id,
                    'project':ta.assigned_project_id,
                    'assigned_date':ta.start_date,
                    'client':ta.client_id,
                    'name':ta.task_name,
                    'deadline':ta.deadline
                })
            completed_task=request.env['employee.task.assignment'].sudo().search([('employee_id','=',employee_ref.id),('status','=','completed')])
            completed_list=[]
            j=0
            for ct in completed_task:
                j=j+1
                completed_list.append({
                    's_no':j,
                    'id':ct.id,
                    'project':ct.assigned_project_id,
                    'task_initiated_time':ct.task_initiated_time,
                    'task_completed_time':ct.task_completed_time,
                    'completed_date':ct.completed_date,
                    'name':ct.task_name,
                    'client':ct.client_id,
                    'deadline':ct.deadline
                })
        return http.request.render('support_sys.view_assigned_tasks', {'employee':employee_ref,'show':show,'task':task_list,'completed':completed_list,'dept':dept_details})



    @http.route('/storeInitiatedTime', auth='user',methods=['POST'],csrf=False)
    def store_initiated_time(self, **kw):
        try:
            # Get data sent with request
            task_id = kw.get('id')
            action = kw.get('action')
            
            current_employee = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
                # current_task = request.env['employee.task.assignment'].sudo().search([('id','=',current_employee.id)])
            current_task = request.env['employee.task.assignment'].sudo().search([('id','=',task_id)],limit=1)
            # Parse the incoming date string
            assigned_time_str = kw.get('assigned_time')
            assigned_time = datetime.strptime(assigned_time_str, '%m/%d/%Y, %I:%M:%S %p')

            # Format the date string in the desired format
            assigned_time_formatted = assigned_time.strftime('%Y-%m-%d %H:%M:%S')
            if action == "initiate":

                current_task.write({
                    'status':'onprogress',
                    'task_initiated_time':assigned_time_formatted
                })
            elif action=="done":
                task_finished_time =  kw.get('assigned_time')
                current_task.write({
                    'status':"completed",
                    'task_completed_time':assigned_time_formatted,
                })               
            else:
                # Invalid action parameter
                return "Invalid action", 400

            # Return a response
            return "Success"
        except Exception as e:
            # Handle exceptions
            return str(e)




