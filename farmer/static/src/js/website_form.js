odoo.define('farmer.website_form', function(require){
	"use strict";
	var publicWidget = require('web.public.widget');
	var core = require('web.core');
	var ajax = require('web.ajax');
	var rpc = require('web.rpc');
	var core = require('web.core');
	var QWeb = core.qweb;
	var _t = core._t;
    var clicked = {};
    var dependencies = {};

	publicWidget.registry.generic_form_data = publicWidget.Widget.extend({
    	selector: '#form_template',
    	events: {
            'click .add_one2manylines_btn': '_onClickAdd_one2manylines',
            'click .remove_line': '_onClickRemove_line',
            'click .custom_create': '_onClickSubmit',
            'focus .many2one_field':'_onFocusMany2OneField',
            'focus .many2many_field':'_onFocusMany2ManyField',
            'change input':'_onUpdateValue',
            'focus #crop_name': '_onFocusMany2ManyField'
        },
        

        _onClickSubmit: async function(ev){
            // checking if all required data is filled before proceeding
            let continueExec = true;
            Array.from(document.querySelectorAll('.many2many_field input')).forEach(e=>{
                if(e.dataset.id){
                    if(e.dataset.id.length==0){
                        continueExec = false;
                        return;
                    }else{
                        e.value=e.dataset.id;
                    }
                }else{
                    continueExec = false;
                    return;
                }
            })
            Array.from(document.querySelectorAll('input[required=True]')).concat(Array.from(document.querySelectorAll('input[required="required"]'))).forEach(e=>{
                if(e.value==''){
                    continueExec = false;
                    return
                }
            })
            if(!continueExec)
                return;
            var self = this;
            var one2many_data = {};
            let data_lines=[];
            let temp={};
            // handling data of one2manuy field type
            Array.from(document.querySelectorAll('#one2many_notebook table')).forEach(table=>{
                data_lines=[]
                Array.from(table.querySelectorAll("tbody .one2many_lines")).forEach(data_input=>{
                    temp={}
                    Array.from(data_input.querySelectorAll('input')).forEach(val=>{
                        if(val.value.length>0)  
                            if(val.classList.contains('select-selected')){
                                temp[val.getAttribute('name')]=val.dataset.id;
                                return;
                            }
                            temp[val.getAttribute('name')]=val.value;
                    })
                    data_lines.push(temp);
                })
                one2many_data[table.dataset.fieldname]=data_lines;
            })
            console.log(one2many_data)
            //handling data of many2one field type
            let many2one_fields = Array.from(document.querySelectorAll('.many2one_field input'))
            many2one_fields.forEach(field=>{
                field.value=field.dataset.id;
            })

            //handling data of many2many field type
            let many2many_fields = Array.from(document.querySelectorAll('.many2many_field input'))
            many2many_fields.forEach(field=>{
                field.value = field.dataset.id.slice(0,field.dataset.id.length-1);
            })
            if( document.getElementById('one2many_data'))   
                document.getElementById('one2many_data').value=JSON.stringify(one2many_data);
        },

        _onClickRemove_line: function(ev){
            console.log("*")
            //removing the selected line from DOM
            ev.target.parentNode.parentNode.remove();
        },

        _onClickAdd_one2manylines: function(ev){
            let target= ev.target;
            if(target.tagName=='I'){
                target=target.parentNode
            }
            //checking if the DOM has loaded completly before executing the function
            if(target.parentNode.parentNode.children[1].lastElementChild.lastElementChild==null){
                return;
            }
            //creating new line
            let new_row=target.parentNode.parentNode.children[1].lastElementChild.lastElementChild.cloneNode(true);
            new_row.classList.remove('select-hide');
            new_row.classList.remove('add_one2manylines');
            new_row.classList.add('one2many_lines');
            //adding new line to the DOM
            target.parentNode.parentNode.children[1].lastElementChild.insertBefore(new_row,target.parentNode.parentNode.children[1].lastElementChild.lastElementChild);
            // adding required=True attributes to the input tags in the newly created lines
            Array.from(target.parentNode.parentNode.children[1].lastElementChild.children).forEach(each=>{
                if(each.classList.contains('select-hide')){
                    return;
                }
                Array.from(each.children).forEach(td=>{
                    Array.from(td.getElementsByClassName('form-control')).forEach(input=>{
                        input.setAttribute("required",true);
                    })
                })
            })
        },

        _onFocusMany2OneField: async function(ev){
            let id = ev.target.parentNode.getAttribute('id');
            console.log(ev.target.getAttribute('domain'));
            let domain = JSON.parse(ev.target.getAttribute('domain'));
            console.log(domain)
            // if domain in kept for the input field
            if(domain){
                domain.forEach(each_domain=>{
                    if(dependencies[each_domain[2]]){
                        if(!dependencies[each_domain[2]].includes(id)){
                            dependencies[each_domain[2]].push(id)
                        }
                    }else{
                        dependencies[each_domain[2]]=[id]
                    }
                    if(typeof each_domain[2]=='string' && document.querySelector('.simple-form #'+each_domain[2]+' input').dataset.id){
                        each_domain[2]=Number(document.querySelector('.simple-form #'+each_domain[2]+' input').dataset.id);
                        clicked[id]=false;
                    }
                })
            }
            if(clicked[id]){
                return;
            }  
            clicked[id]=true;
            let data = await this.readData(ev.target.getAttribute('model'),domain);
            this.clearSelect(ev.target)
            this.styleSelect(ev.target,data)
        },

        _onFocusMany2ManyField: async function(ev){
            let id = ev.target.parentNode.getAttribute('id');
            let domain = JSON.parse(ev.target.getAttribute('domain'));
            // if domain in kept for the input field
            if(domain){
                domain.forEach(each_domain=>{
                    if(dependencies[each_domain[2]]){
                        if(!dependencies[each_domain[2]].includes(id)){
                            dependencies[each_domain[2]].push(id)
                        }
                    }else{
                        dependencies[each_domain[2]]=[id]
                    }
                    if(typeof each_domain[2]=='string' && document.querySelector('.simple-form #'+each_domain[2]+' input').dataset.id){
                        each_domain[2]=Number(document.querySelector('.simple-form #'+each_domain[2]+' input').dataset.id);
                        clicked[id]=false;
                    }
                })
            }
            if(clicked[id]){
                return;
            }  
            clicked[id]=true;
            let data = await this.readData(ev.target.getAttribute('model'),domain);
            this.clearSelect(ev.target)
            this.styleSelectMany2Many(ev.target,data)
        },

        _onUpdateValue: function(ev){
            // if the function is called with event target will be ev.target
            // else it will be ev itself
            let target;
            if(ev.target)
                target=ev.target;
            else
                target=ev;
            let changedId = target.getAttribute('name');
            if(!dependencies[changedId])
                return;
            dependencies[changedId].forEach(each=>{
                document.querySelectorAll("input[name='"+each+"']").forEach(input=>{
                    this._onUpdateValue(input)
                    input.value='';
                    input.dataset.id='';
                })
            })
        },

        async readData(model,domain=[]){
            let data = await this._rpc({
                model: model,
                method: 'search_read',
                args: [domain,['id','display_name']],
            });
            return data;
        },


        styleSelect(target,data){
            let x, i, j, l, ll, selElmnt, a, b, c;
            /*look for any elements with the given id*/
            x = target.parentNode;
            // l = x.length;
            l=1;
            for (i = 0; i < l; i++) {
                selElmnt = data;
                ll = data.length;
                /*a represents selected item*/
                a = x.getElementsByTagName('input')[0];
                a.setAttribute("class", "form-control select-selected");
                a.placeholder = 'Select Here..';
                /*for each element, create a new DIV that will contain the option list:*/
                b = document.createElement("DIV");
                b.setAttribute("class", "select-items select-hide");
                for (j = 0; j < ll; j++) {
                    /*for each option in the original select element,
                    create a new DIV that will act as an option item:*/
                    c = document.createElement("DIV");
                    c.innerHTML = data[j]["display_name"];
                    c.dataset.id = data[j]["id"];
                    b.appendChild(c);
                }
                x.appendChild(b);
                a.addEventListener("click", (e)=> {
                    /*when the input is clicked, close any other select boxes*/
                    this.closeAllSelect(e.target);
                    if(e.target.parentNode.lastElementChild.classList.contains("select-hide"))
                        e.target.parentNode.lastElementChild.classList.remove("select-hide")
                });
            }
            Array.from(b.children).forEach((each)=>{
                each.addEventListener('click',(e)=>{
                    a.value=e.target.innerHTML;
                    this._onUpdateValue(a)
                    a.dataset.id = e.target.dataset.id
                })
            })
            a.addEventListener('input',(e)=>{
                let all_data = Array.from(x.getElementsByClassName('select-items')[0].childNodes)
                if(e.target.value.length==0){
                    all_data.forEach(each=>{
                        if(each.classList.contains('data-hide')){
                            each.classList.remove('data-hide');
                        }
                    })
                }
                all_data.forEach(each=>{
                    if(!each.innerHTML.startsWith(e.target.value)){
                        each.classList.add('data-hide');
                    }else if(each.classList.contains('data-hide')){
                        each.classList.remove('data-hide');
                    }

                })

            })
            /*if the user clicks anywhere outside the select box,
            then close all select boxes:*/
            document.addEventListener("click",(e)=> this.closeAllSelect(e.target));
        },

        styleSelectMany2Many(target,data){
            let x, i, j, l, ll, selElmnt, a, b, c, z;
            /*look for any elements with the given id*/
            x = target.parentNode;
            // l = x.length;
            l=1;
            for (i = 0; i < l; i++) {
                selElmnt = data;
                ll = data.length;
                /* z represents selected items */
                z = document.createElement('DIV');
                z.className='selected-items';
                x.prepend(z);
                z = x.getElementsByClassName('selected-items')[0];
                /*a is used for searchiing*/
                a = x.getElementsByTagName('input')[0];
                a.setAttribute("class", "form-control select-selected");
                a.placeholder = 'Select Here..';
                a.dataset.id='';
                /*for each element, create a new DIV that will contain the option list:*/
                b = document.createElement("DIV");
                b.setAttribute("class", "select-items select-hide");
                for (j = 0; j < ll; j++) {
                    /*for each option in the original select element,
                    create a new DIV that will act as an option item:*/
                    c = document.createElement("DIV");
                    c.innerHTML = data[j]["display_name"];
                    c.dataset.id = data[j]["id"];
                    b.appendChild(c);
                }
                x.appendChild(b);
                a.addEventListener("click", (e)=> {
                    /*when the input is clicked, close any other select boxes*/
                    this.closeAllSelect(e.target);
                    if(e.target.parentNode.lastElementChild.classList.contains("select-hide"))
                        e.target.parentNode.lastElementChild.classList.remove("select-hide")
                });
            }
            Array.from(b.children).forEach((each)=>{
                each.addEventListener('click',(e)=>{
                    // checkiing if the item is already selected
                    if(a.dataset.id.split(',').includes(e.target.dataset.id)){
                        return;
                    }

                    let temp = document.createElement('DIV');
                    temp.className='many2many_selected_tag'
                    temp.innerHTML=e.target.innerHTML;
                    let cross_icon = document.createElement('I');
                    cross_icon.className = 'fa fa-times'
                    cross_icon.dataset.id = e.target.dataset.id
                    cross_icon.addEventListener('click',(e)=>{
                        // removing the selected item after cross icon is pressed
                        let id = e.target.dataset.id;
                        e.target.parentNode.remove();
                        a.dataset.id = a.dataset.id.replace(id+',','');
                    })
                    temp.append(cross_icon)
                    z.append(temp)
                    this._onUpdateValue(a)
                    a.dataset.id += String(e.target.dataset.id)+',';
                })
            })
            a.addEventListener('input',(e)=>{
                let all_data = Array.from(x.getElementsByClassName('select-items')[0].childNodes)
                if(e.target.value.length==0){
                    all_data.forEach(each=>{
                        if(each.classList.contains('data-hide')){
                            each.classList.remove('data-hide');
                        }
                    })
                }
                all_data.forEach(each=>{
                    if(!each.innerHTML.startsWith(e.target.value)){
                        each.classList.add('data-hide');
                    }else if(each.classList.contains('data-hide')){
                        each.classList.remove('data-hide');
                    }

                })

            })
            /*if the user clicks anywhere outside the select box,
            then close all select boxes:*/
            document.addEventListener("click",(e)=> this.closeAllSelect(e.target));
        },

        closeAllSelect(elmnt) {
            /*a function that will close all select boxes in the document,
            except the current select box:*/
            var x, y, i, xl, yl, arrNo = [];
            x = document.getElementsByClassName("select-items");
            y = document.getElementsByClassName("select-selected");
            xl = x.length;
            yl = y.length;
            for (i = 0; i < yl; i++) {
                if (elmnt == y[i]) {
                    arrNo.push(i)
                } else {
                    y[i].classList.remove("select-arrow-active");
                }
            }
            for (i = 0; i < xl; i++) {
                if (arrNo.indexOf(i)) {
                    x[i].classList.add("select-hide");
                }
            }
        },

        clearSelect(target){
            Array.from(target.parentNode.children).forEach(each=>{
                if(each.tagName=='DIV')
                    each.remove()
            })
        },

    });
});