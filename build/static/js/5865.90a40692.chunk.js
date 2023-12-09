(globalThis.webpackChunk_stlite_desktop=globalThis.webpackChunk_stlite_desktop||[]).push([[5865],{26156:(t,e,n)=>{"use strict";n.d(e,{Z:()=>u});var a=n(5057),r=n(66904),i=n.n(r),o=n(52277),s=n.n(o),c=n(96266);const p=({className:t,scriptRunId:e,numParticles:n,numParticleTypes:a,ParticleComponent:r})=>(0,c.jsx)("div",{className:s()(t,"stHidden"),children:i()(n).map((t=>{const n=Math.floor(Math.random()*a);return(0,c.jsx)(r,{particleType:n},e+t)}))}),u=(0,a.memo)(p)},24709:(t,e,n)=>{"use strict";n.r(e),n.d(e,{NUM_FLAKES:()=>d,default:()=>g});var a=n(5057);const r=n.p+"static/media/flake-0.beded754e8024c73d9d2.png",i=n.p+"static/media/flake-1.8077dc154e0bf900aa73.png",o=n.p+"static/media/flake-2.e3f07d06933dd0e84c24.png";var s=n(26156),c=n(45490),p=n(21371);const u=(t,e=0)=>Math.random()*(t-e)+e,l=(0,c.Z)("img",{target:"e1hbdfkw0"})((({theme:t})=>({position:"fixed",top:"-150px",marginLeft:"-75px",zIndex:t.zIndices.balloons,left:`${u(90,10)}vw`,animationDelay:`${u(4e3)}ms`,height:"150px",width:"150px",pointerEvents:"none",animationDuration:"3000ms",animationName:p.F4`
  from {
    transform:
      translateY(0)
      rotateX(${u(360)}deg)
      rotateY(${u(360)}deg)
      rotateZ(${u(360)}deg);
  }

  to {
    transform:
      translateY(calc(100vh + ${150}px))
      rotateX(0)
      rotateY(0)
      rotateZ(0);
  }
`,animationTimingFunction:"ease-in",animationDirection:"normal",animationIterationCount:1,opacity:1})),"");var m=n(96266);const d=100,f=[r,i,o],v=f.length,h=({particleType:t})=>(0,m.jsx)(l,{src:f[t]}),x=function({scriptRunId:t}){return(0,m.jsx)(s.Z,{className:"snow",scriptRunId:t,numParticleTypes:v,numParticles:d,ParticleComponent:h})},g=(0,a.memo)(x)},99980:t=>{var e=Math.ceil,n=Math.max;t.exports=function(t,a,r,i){for(var o=-1,s=n(e((a-t)/(r||1)),0),c=Array(s);s--;)c[i?s:++o]=t,t+=r;return c}},39594:(t,e,n)=>{var a=n(36418),r=/^\s+/;t.exports=function(t){return t?t.slice(0,a(t)+1).replace(r,""):t}},9186:(t,e,n)=>{var a=n(99980),r=n(27396),i=n(17046);t.exports=function(t){return function(e,n,o){return o&&"number"!=typeof o&&r(e,n,o)&&(n=o=void 0),e=i(e),void 0===n?(n=e,e=0):n=i(n),o=void 0===o?e<n?1:-1:i(o),a(e,n,o,t)}}},36418:t=>{var e=/\s/;t.exports=function(t){for(var n=t.length;n--&&e.test(t.charAt(n)););return n}},66904:(t,e,n)=>{var a=n(9186)();t.exports=a},17046:(t,e,n)=>{var a=n(81692),r=1/0,i=17976931348623157e292;t.exports=function(t){return t?(t=a(t))===r||t===-r?(t<0?-1:1)*i:t===t?t:0:0===t?t:0}},81692:(t,e,n)=>{var a=n(39594),r=n(26271),i=n(71490),o=NaN,s=/^[-+]0x[0-9a-f]+$/i,c=/^0b[01]+$/i,p=/^0o[0-7]+$/i,u=parseInt;t.exports=function(t){if("number"==typeof t)return t;if(i(t))return o;if(r(t)){var e="function"==typeof t.valueOf?t.valueOf():t;t=r(e)?e+"":e}if("string"!=typeof t)return 0===t?t:+t;t=a(t);var n=c.test(t);return n||p.test(t)?u(t.slice(2),n?2:8):s.test(t)?o:+t}}}]);