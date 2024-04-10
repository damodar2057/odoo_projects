odoo.define('farmer.styler', async function(require){
    "use strict";
	var core = require('web.core');
	var ajax = require('web.ajax');
	var rpc = require('web.rpc');
	var QWeb = core.qweb;
	var _t = core._t;
    // console.log(core)
    // console.log(QWeb);
    // console.log(rpc);
    // console.log(ajax);

    async function obtainModuleMenuID(){
        let model = "ir.ui.menu"
        let domain = [['name','=','FIS']]
        let data = await rpc.query({
            model: model,
            method: 'search_read',
            args: [domain,['id']],
        });
        return data.map((each)=>each.id);
    }

    let menuIDs =await obtainModuleMenuID();
    let urlMenuID=Number(window.location.href.split('&').pop().split('=').pop());

    
        
    const observeUrlChange = () => {
        let oldHref = document.location.href;
        const body = document.querySelector("body");
        const observer = new MutationObserver(mutations => {
          if (oldHref !== document.location.href) {
            oldHref = document.location.href;
            /* Changed ! your code here */
            let urlMenuID=Number(window.location.href.split('&').pop().split('=').pop());
            // console.log(urlMenuID,menuIDs)
            if(menuIDs.includes(urlMenuID)){
                const myInterval= setInterval(()=>{
                    if(document.getElementsByClassName("o_main_navbar")[0]){
                        clearInterval(myInterval)
                        document.getElementsByClassName("o_main_navbar")[0].style="background-color:red;"
                    }
                },100)
            }else{
                const myInterval= setInterval(()=>{
                    if(document.getElementsByClassName("o_main_navbar")[0]){
                        clearInterval(myInterval)
                        document.getElementsByClassName("o_main_navbar")[0].style=""
                    }
                },100)
            }
          }
        });
        observer.observe(body, { childList: true, subtree: true });
    };
      
    if(menuIDs.includes(urlMenuID)){
        const myInterval= setInterval(()=>{
            if(document.getElementsByClassName("o_main_navbar")[0]){
                clearInterval(myInterval)
                document.getElementsByClassName("o_main_navbar")[0].style="background-color:red;"
            }
        },100)
    }

    window.onload = observeUrlChange;
})