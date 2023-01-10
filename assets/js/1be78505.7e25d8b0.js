"use strict";(self.webpackChunkwiki=self.webpackChunkwiki||[]).push([[514,75],{8704:(e,t,a)=>{a.r(t),a.d(t,{default:()=>J});var n=a(7294),l=a(3905),o=a(6291),c=a(6698),i=a(6010),r=a(941),s=a(3783),d=a(7898),m=a(5537),u=a(7462);const p=e=>n.createElement("svg",(0,u.Z)({width:"20",height:"20","aria-hidden":"true"},e),n.createElement("g",{fill:"#7a7a7a"},n.createElement("path",{d:"M9.992 10.023c0 .2-.062.399-.172.547l-4.996 7.492a.982.982 0 01-.828.454H1c-.55 0-1-.453-1-1 0-.2.059-.403.168-.551l4.629-6.942L.168 3.078A.939.939 0 010 2.528c0-.548.45-.997 1-.997h2.996c.352 0 .649.18.828.45L9.82 9.472c.11.148.172.347.172.55zm0 0"}),n.createElement("path",{d:"M19.98 10.023c0 .2-.058.399-.168.547l-4.996 7.492a.987.987 0 01-.828.454h-3c-.547 0-.996-.453-.996-1 0-.2.059-.403.168-.551l4.625-6.942-4.625-6.945a.939.939 0 01-.168-.55 1 1 0 01.996-.997h3c.348 0 .649.18.828.45l4.996 7.492c.11.148.168.347.168.55zm0 0"})));var b=a(4973),h=a(6742),E=a(3919),f=a(8617);const g="menuLinkText_OKON",k=(e,t)=>"link"===e.type?(0,r.Mg)(e.href,t):"category"===e.type&&e.items.some((e=>k(e,t))),C=(0,n.memo)((function(e){let{items:t,...a}=e;return n.createElement(n.Fragment,null,t.map(((e,t)=>n.createElement(_,(0,u.Z)({key:t,item:e},a)))))}));function _(e){let{item:t,...a}=e;return"category"===t.type?0===t.items.length?null:n.createElement(v,(0,u.Z)({item:t},a)):n.createElement(Z,(0,u.Z)({item:t},a))}function v(e){let{item:t,onItemClick:a,activePath:l,...o}=e;const{items:c,label:s,collapsible:d}=t,m=k(t,l),{collapsed:p,setCollapsed:b,toggleCollapsed:h}=(0,r.uR)({initialState:()=>!!d&&(!m&&t.collapsed)});return function(e){let{isActive:t,collapsed:a,setCollapsed:l}=e;const o=(0,r.D9)(t);(0,n.useEffect)((()=>{t&&!o&&a&&l(!1)}),[t,o,a])}({isActive:m,collapsed:p,setCollapsed:b}),n.createElement("li",{className:(0,i.Z)(r.kM.docs.docSidebarItemCategory,"menu__list-item",{"menu__list-item--collapsed":p})},n.createElement("a",(0,u.Z)({className:(0,i.Z)("menu__link",{"menu__link--sublist":d,"menu__link--active":d&&m,[g]:!d}),onClick:d?e=>{e.preventDefault(),h()}:void 0,href:d?"#":void 0},o),s),n.createElement(r.zF,{lazy:!0,as:"ul",className:"menu__list",collapsed:p},n.createElement(C,{items:c,tabIndex:p?-1:0,onItemClick:a,activePath:l})))}function Z(e){let{item:t,onItemClick:a,activePath:l,...o}=e;const{href:c,label:s}=t,d=k(t,l);return n.createElement("li",{className:(0,i.Z)(r.kM.docs.docSidebarItemLink,"menu__list-item"),key:s},n.createElement(h.Z,(0,u.Z)({className:(0,i.Z)("menu__link",{"menu__link--active":d}),"aria-current":d?"page":void 0,to:c},(0,E.Z)(c)&&{onClick:a},o),(0,E.Z)(c)?s:n.createElement("span",null,s,n.createElement(f.Z,null))))}const N="sidebar_a3j0",S="sidebarWithHideableNavbar_VlPv",T="sidebarHidden_OqfG",I="sidebarLogo_hmkv",M="menu_cyFh",w="menuWithAnnouncementBar_+O1J",y="collapseSidebarButton_eoK2",x="collapseSidebarButtonIcon_e+kA";function B(e){let{onClick:t}=e;return n.createElement("button",{type:"button",title:(0,b.I)({id:"theme.docs.sidebar.collapseButtonTitle",message:"Collapse sidebar",description:"The title attribute for collapse button of doc sidebar"}),"aria-label":(0,b.I)({id:"theme.docs.sidebar.collapseButtonAriaLabel",message:"Collapse sidebar",description:"The title attribute for collapse button of doc sidebar"}),className:(0,i.Z)("button button--secondary button--outline",y),onClick:t},n.createElement(p,{className:x}))}function F(e){let{path:t,sidebar:a,onCollapse:l,isHidden:o}=e;const c=function(){const{isClosed:e}=(0,r.nT)(),[t,a]=(0,n.useState)(!e);return(0,d.Z)((t=>{let{scrollY:n}=t;e||a(0===n)})),t}(),{navbar:{hideOnScroll:s},hideableSidebar:u}=(0,r.LU)(),{isClosed:p}=(0,r.nT)();return n.createElement("div",{className:(0,i.Z)(N,{[S]:s,[T]:o})},s&&n.createElement(m.Z,{tabIndex:-1,className:I}),n.createElement("nav",{className:(0,i.Z)("menu thin-scrollbar",M,{[w]:!p&&c})},n.createElement("ul",{className:(0,i.Z)(r.kM.docs.docSidebarMenu,"menu__list")},n.createElement(C,{items:a,activePath:t}))),u&&n.createElement(B,{onClick:l}))}const P=e=>{let{toggleSidebar:t,sidebar:a,path:l}=e;return n.createElement("ul",{className:(0,i.Z)(r.kM.docs.docSidebarMenu,"menu__list")},n.createElement(C,{items:a,activePath:l,onItemClick:()=>t()}))};function A(e){return n.createElement(r.Cv,{component:P,props:e})}const L=n.memo(F),H=n.memo(A);function D(e){const t=(0,s.Z)(),a="desktop"===t||"ssr"===t,l="mobile"===t;return n.createElement(n.Fragment,null,a&&n.createElement(L,e),l&&n.createElement(H,e))}var R=a(6845),W=a(4608),z=a(6550);const O="backToTopButton_i9tI",Y="backToTopButtonShow_wCmF";function q(){const e=(0,n.useRef)(null);return{smoothScrollTop:function(){e.current=function(){let e=null;return function t(){const a=document.documentElement.scrollTop;a>0&&(e=requestAnimationFrame(t),window.scrollTo(0,Math.floor(.85*a)))}(),()=>e&&cancelAnimationFrame(e)}()},cancelScrollToTop:()=>e.current?.()}}const K=function(){const e=(0,z.TH)(),{smoothScrollTop:t,cancelScrollToTop:a}=q(),[l,o]=(0,n.useState)(!1);return(0,d.Z)(((e,t)=>{let{scrollY:n}=e;if(!t)return;const l=n<t.scrollY;if(l||a(),n<300)o(!1);else if(l){const e=document.documentElement.scrollHeight;n+window.innerHeight<e&&o(!0)}else o(!1)}),[e]),n.createElement("button",{className:(0,i.Z)("clean-btn",O,{[Y]:l}),type:"button",onClick:()=>t()},n.createElement("svg",{viewBox:"0 0 24 24",width:"28"},n.createElement("path",{d:"M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z",fill:"currentColor"})))},U={docPage:"docPage_lDyR",docMainContainer:"docMainContainer_r8cw",docSidebarContainer:"docSidebarContainer_0YBq",docMainContainerEnhanced:"docMainContainerEnhanced_SOUu",docSidebarContainerHidden:"docSidebarContainerHidden_Qlt2",collapsedDocSidebar:"collapsedDocSidebar_zZpm",expandSidebarButtonIcon:"expandSidebarButtonIcon_cxi8",docItemWrapperEnhanced:"docItemWrapperEnhanced_aT5H"};var j=a(9105);function G(e){let{currentDocRoute:t,versionMetadata:a,children:o}=e;const{pluginId:s,version:d}=a,m=t.sidebar,u=m?a.docsSidebars[m]:void 0,[h,E]=(0,n.useState)(!1),[f,g]=(0,n.useState)(!1),k=(0,n.useCallback)((()=>{f&&g(!1),E(!h)}),[f]);return n.createElement(c.Z,{wrapperClassName:r.kM.wrapper.docsPages,pageClassName:r.kM.page.docsDocPage,searchMetadatas:{version:d,tag:(0,r.os)(s,d)}},n.createElement("div",{className:U.docPage},n.createElement(K,null),u&&n.createElement("aside",{className:(0,i.Z)(U.docSidebarContainer,{[U.docSidebarContainerHidden]:h}),onTransitionEnd:e=>{e.currentTarget.classList.contains(U.docSidebarContainer)&&h&&g(!0)}},n.createElement(D,{key:m,sidebar:u,path:t.path,onCollapse:k,isHidden:f}),f&&n.createElement("div",{className:U.collapsedDocSidebar,title:(0,b.I)({id:"theme.docs.sidebar.expandButtonTitle",message:"Expand sidebar",description:"The ARIA label and title attribute for expand button of doc sidebar"}),"aria-label":(0,b.I)({id:"theme.docs.sidebar.expandButtonAriaLabel",message:"Expand sidebar",description:"The ARIA label and title attribute for expand button of doc sidebar"}),tabIndex:0,role:"button",onKeyDown:k,onClick:k},n.createElement(p,{className:U.expandSidebarButtonIcon}))),n.createElement("main",{className:(0,i.Z)(U.docMainContainer,{[U.docMainContainerEnhanced]:h||!u})},n.createElement("div",{className:(0,i.Z)("container padding-top--md padding-bottom--lg",U.docItemWrapper,{[U.docItemWrapperEnhanced]:h})},n.createElement(l.Zo,{components:R.Z},o)))))}const J=function(e){const{route:{routes:t},versionMetadata:a,location:l}=e,c=t.find((e=>(0,z.LX)(l.pathname,e)));return c?n.createElement(n.Fragment,null,n.createElement(j.Z,null,n.createElement("html",{className:a.className})),n.createElement(G,{currentDocRoute:c,versionMetadata:a},(0,o.Z)(t,{versionMetadata:a}))):n.createElement(W.default,e)}},4608:(e,t,a)=>{a.r(t),a.d(t,{default:()=>c});var n=a(7294),l=a(6698),o=a(4973);const c=function(){return n.createElement(l.Z,{title:(0,o.I)({id:"theme.NotFound.title",message:"Page Not Found"})},n.createElement("main",{className:"container margin-vert--xl"},n.createElement("div",{className:"row"},n.createElement("div",{className:"col col--6 col--offset-3"},n.createElement("h1",{className:"hero__title"},n.createElement(o.Z,{id:"theme.NotFound.title",description:"The title of the 404 page"},"Page Not Found")),n.createElement("p",null,n.createElement(o.Z,{id:"theme.NotFound.p1",description:"The first paragraph of the 404 page"},"We could not find what you were looking for.")),n.createElement("p",null,n.createElement(o.Z,{id:"theme.NotFound.p2",description:"The 2nd paragraph of the 404 page"},"Please contact the owner of the site that linked you to the original URL and let them know their link is broken."))))))}}}]);