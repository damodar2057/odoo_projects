from odoo import models, fields, _, api


class FarmerGroupMetadata(models.TransientModel):
    _name="farmer.group.metadata"
    
    yearly_investment=fields.Integer(_("Yearly Investment"))
    yearly_transaction=fields.Integer(_("Yearly Transaction"))
    min_monthly_income=fields.Integer(_("Min Income/Month"))
    family_contribution=fields.Integer(_("Family Contribution"))
    num_employees=fields.Integer(_("No. of Employees"))
    num_experience=fields.Integer(_("No. Experiences"))
    ability_and_technology=fields.Selection(selection=[
        ('trained_and_advanced_tech','Trained and Advanced Tech'),
        ('trained_and_mid_tech','Trained and Mid Tech'),
        ('mid_tech','Mid Tech'),
        ('mixed','Mixed')],string="Ability and Technology")

    def assign_farmer_group(self,vals):
        farmer_group_orm=self.env["farmer.type"]
        farmer_groups=farmer_group_orm.search([])
        
        ability_and_technology=vals.get('ability_and_technology')
        num_experience=vals.get('num_experience')
        num_employees=vals.get('num_employees')
        family_contribution=vals.get('family_contribution')
        min_monthly_income=vals.get('min_monthly_income')
        yearly_transaction=vals.get('yearly_transaction')
        yearly_investment=vals.get('yearly_investment')
        match_group=None
        match_value_counts=0
        
        for group in farmer_groups:
            check_num_experience=group._check_range('num_experience',num_experience,id=group.id,is_gte=True)
            check_num_employees=group._check_range('num_employees',num_employees,is_gte=False,id=group.id)
            check_family_contribution=group._check_range('family_contribution',family_contribution,id=group.id,is_gte=False)
            check_min_monthly_income=group._check_range('min_monthly_income',min_monthly_income,id=group.id,is_gte=True)
            check_yearly_transaction=group._check_range('yearly_transaction',yearly_transaction,is_gte=False,id=group.id)
            check_yearly_investment=group._check_range('yearly_investment',yearly_investment,is_gte=False,id=group.id)
            check_ability_and_technology_truth=ability_and_technology==group.ability_and_technology
            group_truth_values=[check_num_experience,check_num_employees,check_family_contribution,check_min_monthly_income,check_yearly_transaction,check_yearly_investment,check_ability_and_technology_truth]
            print(group_truth_values)
            curr_match_value_counts=sum(group_truth_values)
            print(group_truth_values,curr_match_value_counts,group.id)
            if curr_match_value_counts > match_value_counts:
                match_group=group
                match_value_counts=curr_match_value_counts
        print(match_group)
        
        return match_group
    
    @api.model
    def create(self, vals):
        recommended_farmer_group=self.assign_farmer_group(vals)
        print(vals)
        if recommended_farmer_group:
            farmer = self.env['farm.farmer'].search([['id','=',self._context['active_id']]])
            farmer.farmer_group = recommended_farmer_group
            farmer.yearly_investment = vals.get('yearly_investment')
            farmer.yearly_transaction = vals.get('yearly_transaction')
            farmer.min_monthly_income = vals.get('min_monthly_income')
            farmer.family_contribution = vals.get('family_contribution')
            farmer.num_employees = vals.get('num_employees')
            farmer.num_experience = vals.get('num_experience')
            farmer.ability_and_technology = vals.get('ability_and_technology')
        return super(FarmerGroupMetadata, self).create(vals)
