"use strict";(globalThis.webpackChunk_stlite_desktop=globalThis.webpackChunk_stlite_desktop||[]).push([[6242],{32523:(e,t,i)=>{i.r(t),i.d(t,{default:()=>u});var s=i(5057),o=i(56846),l=i(40691),a=i(34422),r=i(96266);class n extends s.PureComponent{constructor(...e){super(...e),this.formClearHelper=new o.Kz,this.state={value:this.initialValue},this.commitWidgetValue=e=>{this.props.widgetMgr.setStringValue(this.props.element,this.state.value,e)},this.onFormCleared=()=>{this.setState(((e,t)=>({value:t.element.default})),(()=>this.commitWidgetValue({fromUi:!0})))},this.onColorClose=e=>{this.setState({value:e},(()=>this.commitWidgetValue({fromUi:!0})))}}get initialValue(){const e=this.props.widgetMgr.getStringValue(this.props.element);return void 0!==e?e:this.props.element.default}componentDidMount(){this.props.element.setValue?this.updateFromProtobuf():this.commitWidgetValue({fromUi:!1})}componentDidUpdate(){this.maybeUpdateFromProtobuf()}componentWillUnmount(){this.formClearHelper.disconnect()}maybeUpdateFromProtobuf(){const{setValue:e}=this.props.element;e&&this.updateFromProtobuf()}updateFromProtobuf(){const{value:e}=this.props.element;this.props.element.setValue=!1,this.setState({value:e},(()=>{this.commitWidgetValue({fromUi:!1})}))}render(){var e;const{element:t,width:i,disabled:s,widgetMgr:o}=this.props,{value:n}=this.state;return this.formClearHelper.manageFormClearListener(o,t.formId,this.onFormCleared),(0,r.jsx)(l.Z,{label:t.label,labelVisibility:(0,a.iF)(null===(e=t.labelVisibility)||void 0===e?void 0:e.value),help:t.help,onChange:this.onColorClose,disabled:s,width:i,value:n})}}const u=n}}]);