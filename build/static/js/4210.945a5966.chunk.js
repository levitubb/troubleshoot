(globalThis.webpackChunk_stlite_desktop=globalThis.webpackChunk_stlite_desktop||[]).push([[4210],{44210:(e,t,o)=>{"use strict";o.r(t),o.d(t,{default:()=>S});var r=o(5057),s=o(11226),i=o(78164),n=o.n(i),l=o(31476),a=o(56846),p=o(94861),u=o(87118),d=o(86964);const h=(0,o(45490).Z)("div",{target:"ede6r8z0"})((({theme:e})=>({"span[aria-disabled='true']":{background:e.colors.fadedText05}})),"");var c=o(8429),m=o(54840),g=o(95323),f=o(58269),v=o(34422),b=o(96266);class x extends r.PureComponent{constructor(...e){super(...e),this.formClearHelper=new a.Kz,this.state={value:this.initialValue},this.commitWidgetValue=e=>{this.props.widgetMgr.setIntArrayValue(this.props.element,this.state.value,e)},this.onFormCleared=()=>{this.setState(((e,t)=>({value:t.element.default})),(()=>this.commitWidgetValue({fromUi:!0})))},this.onChange=e=>{this.props.element.maxSelections&&"select"===e.type&&this.state.value.length>=this.props.element.maxSelections||this.setState(this.generateNewState(e),(()=>{this.commitWidgetValue({fromUi:!0})}))},this.filterOptions=(e,t)=>{if(this.overMaxSelections())return[];const o=e.filter((e=>!this.state.value.includes(Number(e.value))));return(0,f.H)(o,t)}}overMaxSelections(){return this.props.element.maxSelections>0&&this.state.value.length>=this.props.element.maxSelections}getNoResultsMsg(){if(0===this.props.element.maxSelections)return"No results";const e=1!==this.props.element.maxSelections?"options":"option";return`You can only select up to ${this.props.element.maxSelections} ${e}. Remove an option first.`}get initialValue(){const e=this.props.widgetMgr.getIntArrayValue(this.props.element);return void 0!==e?e:this.props.element.default}componentDidMount(){this.props.element.setValue?this.updateFromProtobuf():this.commitWidgetValue({fromUi:!1})}componentDidUpdate(){this.maybeUpdateFromProtobuf()}componentWillUnmount(){this.formClearHelper.disconnect()}maybeUpdateFromProtobuf(){const{setValue:e}=this.props.element;e&&this.updateFromProtobuf()}updateFromProtobuf(){const{value:e}=this.props.element;this.props.element.setValue=!1,this.setState({value:e},(()=>{this.commitWidgetValue({fromUi:!1})}))}get valueFromState(){return this.state.value.map((e=>{const t=this.props.element.options[e];return{value:e.toString(),label:t}}))}generateNewState(e){const t=()=>{var t;const o=null===(t=e.option)||void 0===t?void 0:t.value;return parseInt(o,10)};switch(e.type){case"remove":return{value:n()(this.state.value,t())};case"clear":return{value:[]};case"select":return{value:this.state.value.concat([t()])};default:throw new Error(`State transition is unknown: ${e.type}`)}}render(){var e;const{element:t,theme:o,width:r,widgetMgr:i}=this.props,n={width:r},{options:l}=t,a=0===l.length||this.props.disabled,f=0===l.length?"No options to select.":"Choose an option",x=l.map(((e,t)=>({label:e,value:t.toString()})));this.formClearHelper.manageFormClearListener(i,t.formId,this.onFormCleared);const S=l.length>10;return(0,b.jsxs)("div",{className:"row-widget stMultiSelect",style:n,children:[(0,b.jsx)(d.ON,{label:t.label,disabled:a,labelVisibility:(0,v.iF)(null===(e=t.labelVisibility)||void 0===e?void 0:e.value),children:t.help&&(0,b.jsx)(d.dT,{children:(0,b.jsx)(c.ZP,{content:t.help,placement:m.ug.TOP_RIGHT})})}),(0,b.jsx)(h,{children:(0,b.jsx)(p.Z,{options:x,labelKey:"label",valueKey:"value","aria-label":t.label,placeholder:f,type:u.wD.select,multi:!0,onChange:this.onChange,value:this.valueFromState,disabled:a,size:"compact",noResultsMsg:this.getNoResultsMsg(),filterOptions:this.filterOptions,closeOnSelect:!1,overrides:{IconsContainer:{style:()=>({paddingRight:".5rem"})},ControlContainer:{style:{borderLeftWidth:"1px",borderRightWidth:"1px",borderTopWidth:"1px",borderBottomWidth:"1px"}},Placeholder:{style:()=>({flex:"inherit"})},ValueContainer:{style:()=>({minHeight:"38.4px",paddingLeft:".5rem",paddingTop:0,paddingBottom:0,paddingRight:0})},ClearIcon:{props:{overrides:{Svg:{style:{color:o.colors.darkGray}}}}},SearchIcon:{style:{color:o.colors.darkGray}},Tag:{props:{overrides:{Root:{style:{borderTopLeftRadius:o.radii.md,borderTopRightRadius:o.radii.md,borderBottomRightRadius:o.radii.md,borderBottomLeftRadius:o.radii.md,fontSize:o.fontSizes.sm,paddingLeft:o.spacing.sm,marginLeft:0,marginRight:o.spacing.sm,height:"28px"}},Action:{style:{paddingLeft:0}},ActionIcon:{props:{overrides:{Svg:{style:{width:"10px",height:"10px"}}}}},Text:{style:{fontSize:o.fontSizes.md}}}}},MultiValue:{props:{overrides:{Root:{style:{fontSize:o.fontSizes.sm}}}}},Input:{props:{readOnly:s.tq&&!1===S?"readonly":null}},Dropdown:{component:g.s}}})})]})}}const S=(0,l.b)(x)},97247:(e,t,o)=>{var r=o(54305);e.exports=function(e,t){return!!(null==e?0:e.length)&&r(e,t,0)>-1}},89479:e=>{e.exports=function(e,t,o){for(var r=-1,s=null==e?0:e.length;++r<s;)if(o(t,e[r]))return!0;return!1}},3895:(e,t,o)=>{var r=o(98323),s=o(97247),i=o(89479),n=o(73470),l=o(74631),a=o(51565),p=200;e.exports=function(e,t,o,u){var d=-1,h=s,c=!0,m=e.length,g=[],f=t.length;if(!m)return g;o&&(t=n(t,l(o))),u?(h=i,c=!1):t.length>=p&&(h=a,c=!1,t=new r(t));e:for(;++d<m;){var v=e[d],b=null==o?v:o(v);if(v=u||0!==v?v:0,c&&b===b){for(var x=f;x--;)if(t[x]===b)continue e;g.push(v)}else h(t,b,u)||g.push(v)}return g}},60238:e=>{e.exports=function(e,t,o,r){for(var s=e.length,i=o+(r?1:-1);r?i--:++i<s;)if(t(e[i],i,e))return i;return-1}},54305:(e,t,o)=>{var r=o(60238),s=o(24981),i=o(23481);e.exports=function(e,t,o){return t===t?i(e,t,o):r(e,s,o)}},24981:e=>{e.exports=function(e){return e!==e}},23481:e=>{e.exports=function(e,t,o){for(var r=o-1,s=e.length;++r<s;)if(e[r]===t)return r;return-1}},78164:(e,t,o)=>{var r=o(3895),s=o(86456),i=o(7244),n=s((function(e,t){return i(e)?r(e,t):[]}));e.exports=n}}]);