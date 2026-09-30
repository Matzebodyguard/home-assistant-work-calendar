class WorkCalendarCard extends HTMLElement {
  static getStubConfig(){return {};}
  static async getConfigElement(){return document.createElement("work-calendar-card-editor");}
  setConfig(config){if(!config)throw new Error("Ungültige Konfiguration");this.config=config;}
  set hass(hass){this._hass=hass;if(!this._built)this._build();this._refresh();}
  getCardSize(){return 4;}
  _build(){
    this._built=true;
    this.innerHTML=`<ha-card header="Arbeitskalender"><div style="padding:0 16px 16px"><div id="stats" style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px"></div><div style="display:grid;gap:8px"><button id="today">Heute gearbeitet</button><button id="yesterday">Gestern gearbeitet</button><button id="other">Anderen Arbeitstag eintragen</button></div></div></ha-card>`;
    for(const b of this.querySelectorAll("button"))b.style.cssText="padding:12px;border:0;border-radius:10px;background:var(--primary-color);color:var(--text-primary-color);font:inherit;cursor:pointer";
    this.querySelector("#today").onclick=()=>this._press("today");
    this.querySelector("#yesterday").onclick=()=>this._press("yesterday");
    this.querySelector("#other").onclick=()=>this._dialog();
  }
  _entity(kind){
    const explicit=this.config?.[kind];if(explicit)return explicit;
    const ids=Object.keys(this._hass?.states||{});
    const domain=kind==="today"||kind==="yesterday"?"button.":"sensor.";
    const needles={today:["heute_gearbeitet","worked_today"],yesterday:["gestern_gearbeitet","worked_yesterday"],days_this_month:["days_this_month","arbeitstage_diesen_monat"],days_last_month:["days_last_month","arbeitstage_letzten_monat"]}[kind]||[kind];
    return ids.find(id=>id.startsWith(domain)&&needles.some(n=>id.includes(n)));
  }
  _refresh(){
    if(!this._built||!this._hass)return;
    const val=id=>id&&this._hass.states[id]?this._hass.states[id].state:"–";
    this.querySelector("#stats").innerHTML=`<div><b style="font-size:28px">${val(this._entity("days_this_month"))}</b><br><small>Arbeitstage diesen Monat</small></div><div><b style="font-size:28px">${val(this._entity("days_last_month"))}</b><br><small>Arbeitstage letzten Monat</small></div>`;
  }
  async _press(kind){const id=this._entity(kind);if(id)await this._hass.callService("button","press",{entity_id:id});}
  _dialog(){
    const d=document.createElement("dialog");d.style.cssText="border:0;border-radius:16px;padding:20px;min-width:300px;background:var(--card-background-color);color:var(--primary-text-color)";
    const now=new Date(),today=`${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,"0")}-${String(now.getDate()).padStart(2,"0")}`;
    d.innerHTML=`<h3>Arbeitstag eintragen</h3><label>Datum<br><input id="d" type="date" value="${today}"></label><br><br><label>Beginn<br><input id="s" type="time" value="17:00"></label><br><br><label>Ende<br><input id="e" type="time" value="21:00"></label><br><br><div style="display:flex;justify-content:flex-end;gap:8px"><button id="cancel">Abbrechen</button><button id="save">Eintragen</button></div>`;
    document.body.appendChild(d);
    d.querySelector("#cancel").onclick=()=>{d.close();d.remove();};
    d.querySelector("#save").onclick=async()=>{const data={date:d.querySelector("#d").value,start_time:d.querySelector("#s").value,end_time:d.querySelector("#e").value};if(this.config?.config_entry_id)data.config_entry_id=this.config.config_entry_id;await this._hass.callService("work_calendar","add_workday",data);d.close();d.remove();};
    d.showModal();
  }
}
class WorkCalendarCardEditor extends HTMLElement{
  setConfig(config){this.config=config||{};this.innerHTML="<div style='padding:12px'>Work Calendar benötigt bei einer einzelnen Integration keine weitere Konfiguration.</div>";}
  set hass(hass){this._hass=hass;}
}
if(!customElements.get("work-calendar-card"))customElements.define("work-calendar-card",WorkCalendarCard);
if(!customElements.get("work-calendar-card-editor"))customElements.define("work-calendar-card-editor",WorkCalendarCardEditor);
window.customCards=window.customCards||[];
if(!window.customCards.some(c=>c.type==="work-calendar-card"))window.customCards.push({type:"work-calendar-card",name:"Work Calendar",description:"Arbeitskalender mit Monatszählern und Schnelleinträgen",preview:true});
