/* @odoo-module */

var commonLeafletMap2=require('vehicle_tracking.leaflet_initialization_vehicle_track')
import {registry} from '@web/core/registry';
import {useService} from "@web/core/utils/hooks";
import { useBus } from '@web/core/utils/hooks';
const {Component,onWillStart,onMounted,useState,onWillUnmount,onWillUpdate}=owl;

export class TrackVehicle extends Component{
setup(){
console.log("js setup completed")
this.state=useState({
status:{license_plate:'',model_id:'',driver_id:'',status:'',latitude:'',longitude:''},
allList:[],
responseFromServer:'',
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
markers:false,
number:1,
})
this.orm=useService('orm')
this.model='fleet.vehicle'

onWillStart(async()=>{
await this.getAllStatus();
await this.getRunningStatus();
await this.getActiveStatus();
await this.getInactiveStatus();
await this.getContactlessStatus();
})
onMounted(async()=>{
await this.getMap();
await this.getMapContents();

//await this.getCurrentLocation();
//await this.callMethod()
 this.intervalId=setInterval(async () => {

            await this.getAllStatus();
            await this.getRunningStatus();
            await this.getActiveStatus();
            await this.getInactiveStatus();
            await this.getContactlessStatus();
            await this.clearMarkers();
            await this.getMapContents()
 if(this.state.number==1){
    this.state.allList=this.state.allstatusList
 }
  if(this.state.number==2){
this.state.allList=this.state.runningstatusList
 } if(this.state.number==3){
this.state.allList=this.state.activestatusList
 } if(this.state.number==4){
this.state.allList=this.state.inactivestatusList
 } if(this.state.number==5){
this.state.allList=this.state.contactlessstatusList
 }
        }, 10000);
})
onWillUnmount(()=>{
   console.log("onWillUnmount called")
        clearInterval(this.intervalId);
        commonLeafletMap2.mapRemove();
})
}

async getAllStatus(){
this.state.allstatusList=await this.orm.searchRead(this.model,[],["license_plate","model_id","driver_id",'status','latitude','longitude'])
this.state.allStatusLength=this.state.allstatusList.length
if(this.state.number==1){
this.state.allList=this.state.allstatusList
}
console.log(this.state.allstatusList)
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
this.state.number=2
commonLeafletMap2.clearAllMarker()
this.getMapContents();
}

activeClick(){
this.state.allList=this.state.activestatusList;
this.state.number=3
commonLeafletMap2.clearAllMarker()
this.getMapContents();
}

inactiveClick(){
this.state.allList=this.state.inactivestatusList;
this.state.number=4
commonLeafletMap2.clearAllMarker()
this.getMapContents();
}

contactlessClick(){
this.state.allList=this.state.contactlessstatusList;
this.state.number=5
commonLeafletMap2.clearAllMarker()
 this.getMapContents();
}

allClick(){
this.state.allList=this.state.allstatusList;
this.state.number=1
commonLeafletMap2.clearAllMarker()
this.getMapContents();
}
async getMap(){
commonLeafletMap2.initializeCommonLeafletMap('track_vehicle_map')
}
//async getCurrentLocation(){
//commonLeafletMap2.onLeafletLoad(()=>{
//commonLeafletMap2.getGeolocation()
//})
//}
async clearMarkers(){
commonLeafletMap2.clearAllMarker()
}
async getMapContents(){
//if(this.state.marker===true){
//commonLeafletMap2.clearAllMarker()
//}
var vehicles=this.state.allList
commonLeafletMap2.onLeafletLoad(()=>{
vehicles.map((a,index)=>{
commonLeafletMap2.pointVehicles(a.latitude,a.longitude,a.license_plate)
})
})
//this.state.marker=true

}
loadMap(lat,lng){
commonLeafletMap2.setView_ofVehicle(lat,lng)
}

}

TrackVehicle.template='track.vehicle.leaflet'
registry.category('actions').add('track.vehicle.owl.registry',TrackVehicle)