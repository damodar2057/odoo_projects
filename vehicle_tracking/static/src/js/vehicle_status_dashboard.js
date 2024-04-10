/* @odoo-module */

var commonLeafletMap=require('vehicle_tracking.leaflet_initialization')
import {registry} from '@web/core/registry';
import {useService} from "@web/core/utils/hooks";
const {Component,useRef,onMounted,useState,onWillStart}=owl;

//const {loadJS} from "@web/core/assets"

export class VehicleStatus extends Component{
setup(){
this.state=useState({
status:{license_plate:'',model_id:'',driver_id:'',status:'',latitude:'',longitude:''},
allList:[],
isInitialized:false,
allstatusList:[],
activestatusList:[],
inactivestatusList:[],
runningstatusList:[],
contactlessstatusList:[],
allStatusLength:null,
activeStatusLength:null,
inactiveStatusLength:null,
runningStatusLength:null,
contactlessStatusLength:null,
})
this.orm=useService('orm')
this.model='fleet.vehicle'
this.chartRef=useRef("chart")
onWillStart(async()=>{
await this.LoadJS();
await this.getAllStatus();
await this.getRunningStatus();
await this.getActiveStatus();
await this.getInactiveStatus();
await this.getContactlessStatus();
})
onMounted(async()=>{
await this.waitForChartJS();
const labels = ['Running','Active','Inactive','Out of contact']
  new Chart(
   this.chartRef.el,
    {
      type: 'bar',
     data : {
  labels: labels,
  datasets: [{
    label: 'Vehicle Status',
    data: [this.state.runningStatusLength, this.state.activeStatusLength, this.state.inactiveStatusLength,this.state.contactlessStatusLength,],
    backgroundColor: [
     'rgba(19, 252, 3,0.8)',
      'rgba(11, 3, 252,0.8)',
      'rgba(252, 248, 3, 0.8)',
     'rgba(252, 3, 3, 0.8)',
    ],
    borderColor: [
      'rgb(19, 252, 3)',
      'rgba(11, 3, 252)',
      'rgb(252, 248, 3)',
      'rgb(252, 3, 3)',
    ],
    borderWidth: 2
  }]
},
 options: {
 responsive:true,
 plugins:{

 legend:{

 position:'bottom',
 },
 },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  },
    }
  );

})
}
async LoadJS(){
const chartjs = document.createElement('script');
        chartjs.src = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js';
        chartjs.async = true;
        document.head.appendChild(chartjs);

        return new Promise((resolve)=>{
          chartjs.onload=()=>{
        console.log("chartjs loaded")
        resolve();
        }
        })
}
async waitForChartJS() {
    // Ensure Chart.js is loaded before proceeding
    if (typeof Chart === 'undefined') {
      console.warn("Chart.js is not loaded yet. Waiting...");
      await new Promise(resolve => setTimeout(resolve, 100));
      await this.waitForChartJS();
    }
  }

async getAllStatus(){
this.state.allstatusList=await this.orm.searchRead(this.model,[],["license_plate","model_id","driver_id",'status','latitude','longitude'])
this.state.allStatusLength=this.state.allstatusList.length
this.state.allList=this.state.allstatusList
}

async getRunningStatus(){
this.state.runningstatusList=await this.orm.searchRead(this.model,[['status','=','running']],["license_plate","model_id","driver_id",'status','latitude','longitude'])
this.state.runningStatusLength=this.state.runningstatusList.length
}

async getActiveStatus(){
this.state.activestatusList=await this.orm.searchRead(this.model,[['status','=','active']],["license_plate","model_id","driver_id",'status','latitude','longitude'])
this.state.activeStatusLength=this.state.activestatusList.length
}

async getInactiveStatus(){
this.state.inactivestatusList=await this.orm.searchRead(this.model,[['status','=','inactive']],["license_plate","model_id","driver_id",'status','latitude','longitude'])
this.state.inactiveStatusLength=this.state.inactivestatusList.length
}

async getContactlessStatus(){
this.state.contactlessstatusList=await this.orm.searchRead(this.model,[['status','=','out of contact']],["license_plate","model_id","driver_id",'status','latitude','longitude'])
this.state.contactlessStatusLength=this.state.contactlessstatusList.length
}

runningClick(){
this.state.allList=this.state.runningstatusList;
console.log(this.state.allList)
}

activeClick(){
this.state.allList=this.state.activestatusList;
}

inactiveClick(){
this.state.allList=this.state.inactivestatusList;
}

contactlessClick(){
this.state.allList=this.state.contactlessstatusList;
}

allClick(){
this.state.allList=this.state.allstatusList;
}

loadMap(lat,lng){
if(this.state.isInitialized===true){
commonLeafletMap.mapRemove()
this.state.isInitialized=false
}
if(this.state.isInitialized===false){
commonLeafletMap.initializeCommonLeafletMap('map5')
commonLeafletMap.onLeafletLoad(()=>{
console.log(lat,lng)
commonLeafletMap.pointMarker(lat,lng)
})
this.state.isInitialized=true
}
}


}

VehicleStatus.template='vehicle.status.dashboard'
registry.category('actions').add('vehicle.dashboard.owl.use',VehicleStatus)