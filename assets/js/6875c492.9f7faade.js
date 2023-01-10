"use strict";(self.webpackChunkwiki=self.webpackChunkwiki||[]).push([[610],{6165:(e,t,a)=>{a.d(t,{Z:()=>E});var r=a(7294),n=a(6010),l=a(6698),s=a(6742);const c="sidebar_q+wC",o="sidebarItemTitle_9G5K",m="sidebarItemList_6T4b",i="sidebarItem_cjdF",d="sidebarItemLink_zyXk",u="sidebarItemLinkActive_wcJs";var g=a(4973);function h(e){let{sidebar:t}=e;return 0===t.items.length?null:r.createElement("nav",{className:(0,n.Z)(c,"thin-scrollbar"),"aria-label":(0,g.I)({id:"theme.blog.sidebar.navAriaLabel",message:"Blog recent posts navigation",description:"The ARIA label for recent posts in the blog sidebar"})},r.createElement("div",{className:(0,n.Z)(o,"margin-bottom--md")},t.title),r.createElement("ul",{className:m},t.items.map((e=>r.createElement("li",{key:e.permalink,className:i},r.createElement(s.Z,{isNavLink:!0,to:e.permalink,className:d,activeClassName:u},e.title))))))}var p=a(571);const E=function(e){const{sidebar:t,toc:a,children:s,...c}=e,o=t&&t.items.length>0;return r.createElement(l.Z,c,r.createElement("div",{className:"container margin-vert--lg"},r.createElement("div",{className:"row"},o&&r.createElement("aside",{className:"col col--3"},r.createElement(h,{sidebar:t})),r.createElement("main",{className:(0,n.Z)("col",{"col--7":o,"col--9 col--offset-1":!o}),itemScope:!0,itemType:"http://schema.org/Blog"},s),a&&r.createElement("div",{className:"col col--2"},r.createElement(p.Z,{toc:a})))))}},4884:(e,t,a)=>{a.d(t,{Z:()=>N});var r=a(7294),n=a(6010),l=a(3905),s=a(4973),c=a(6742),o=a(4996),m=a(941),i=a(6845),d=a(6146);const u="blogPostTitle_d4p0",g="blogPostData_-Im+",h="blogPostDetailsFull_xD8n";var p=a(7682);const E="image_9q7L";const f=function(e){let{author:t}=e;const{name:a,title:n,url:l,imageURL:s}=t;return r.createElement("div",{className:"avatar margin-bottom--sm"},s&&r.createElement(c.Z,{className:"avatar__photo-link avatar__photo",href:l},r.createElement("img",{className:E,src:s,alt:a})),a&&r.createElement("div",{className:"avatar__intro",itemProp:"author",itemScope:!0,itemType:"https://schema.org/Person"},r.createElement("div",{className:"avatar__name"},r.createElement(c.Z,{href:l,itemProp:"url"},r.createElement("span",{itemProp:"name"},a))),n&&r.createElement("small",{className:"avatar__subtitle",itemProp:"description"},n)))},b="authorCol_8c0z";function v(e){let{authors:t,assets:a}=e;return 0===t.length?r.createElement(r.Fragment,null):r.createElement("div",{className:"row margin-top--md margin-bottom--sm"},t.map(((e,t)=>r.createElement("div",{className:(0,n.Z)("col col--6",b),key:t},r.createElement(f,{author:{...e,imageURL:a.authorsImageUrls[t]??e.imageURL}})))))}const N=function(e){const t=function(){const{selectMessage:e}=(0,m.c2)();return t=>{const a=Math.ceil(t);return e(a,(0,s.I)({id:"theme.blog.post.readingTime.plurals",description:'Pluralized label for "{readingTime} min read". Use as much plural forms (separated by "|") as your language support (see https://www.unicode.org/cldr/cldr-aux/charts/34/supplemental/language_plural_rules.html)',message:"One min read|{readingTime} min read"},{readingTime:a}))}}(),{withBaseUrl:a}=(0,o.C)(),{children:E,frontMatter:f,assets:b,metadata:N,truncated:_,isBlogPostPage:k=!1}=e,{date:Z,formattedDate:P,permalink:T,tags:w,readingTime:L,title:y,editUrl:C,authors:I}=N,M=b.image??f.image;return r.createElement("article",{className:k?void 0:"margin-bottom--xl",itemProp:"blogPost",itemScope:!0,itemType:"http://schema.org/BlogPosting"},(()=>{const e=k?"h1":"h2";return r.createElement("header",null,r.createElement(e,{className:u,itemProp:"headline"},k?y:r.createElement(c.Z,{itemProp:"url",to:T},y)),r.createElement("div",{className:(0,n.Z)(g,"margin-vert--md")},r.createElement("time",{dateTime:Z,itemProp:"datePublished"},P),void 0!==L&&r.createElement(r.Fragment,null," \xb7 ",t(L))),r.createElement(v,{authors:I,assets:b}))})(),M&&r.createElement("meta",{itemProp:"image",content:a(M,{absolute:!0})}),r.createElement("div",{className:"markdown",itemProp:"articleBody"},r.createElement(l.Zo,{components:i.Z},E)),(w.length>0||_)&&r.createElement("footer",{className:(0,n.Z)("row docusaurus-mt-lg",{[h]:k})},w.length>0&&r.createElement("div",{className:(0,n.Z)("col",{"col--9":!k})},r.createElement(p.Z,{tags:w})),k&&C&&r.createElement("div",{className:"col margin-top--sm"},r.createElement(d.Z,{editUrl:C})),!k&&_&&r.createElement("div",{className:"col col--3 text--right"},r.createElement(c.Z,{to:N.permalink,"aria-label":`Read more about ${y}`},r.createElement("b",null,r.createElement(s.Z,{id:"theme.blog.post.readMore",description:"The label used in blog post item excerpts to link to full blog posts"},"Read More"))))))}},9404:(e,t,a)=>{a.r(t),a.d(t,{default:()=>m});var r=a(7294),n=a(6742),l=a(6165),s=a(4884),c=a(4973),o=a(941);function m(e){const{metadata:t,items:a,sidebar:m}=e,{allTagsPath:i,name:d,count:u}=t,g=function(){const{selectMessage:e}=(0,o.c2)();return t=>e(t,(0,c.I)({id:"theme.blog.post.plurals",description:'Pluralized label for "{count} posts". Use as much plural forms (separated by "|") as your language support (see https://www.unicode.org/cldr/cldr-aux/charts/34/supplemental/language_plural_rules.html)',message:"One post|{count} posts"},{count:t}))}(),h=(0,c.I)({id:"theme.blog.tagTitle",description:"The title of the page for a blog tag",message:'{nPosts} tagged with "{tagName}"'},{nPosts:g(u),tagName:d});return r.createElement(l.Z,{title:h,wrapperClassName:o.kM.wrapper.blogPages,pageClassName:o.kM.page.blogTagPostListPage,searchMetadatas:{tag:"blog_tags_posts"},sidebar:m},r.createElement("header",{className:"margin-bottom--xl"},r.createElement("h1",null,h),r.createElement(n.Z,{href:i},r.createElement(c.Z,{id:"theme.tags.tagsPageLink",description:"The label of the link targeting the tag list page"},"View All Tags"))),a.map((e=>{let{content:t}=e;return r.createElement(s.Z,{key:t.metadata.permalink,frontMatter:t.frontMatter,assets:t.assets,metadata:t.metadata,truncated:!0},r.createElement(t,null))})))}},6146:(e,t,a)=>{a.d(t,{Z:()=>i});var r=a(7294),n=a(4973),l=a(7462),s=a(6010);const c="iconEdit_mS5F",o=e=>{let{className:t,...a}=e;return r.createElement("svg",(0,l.Z)({fill:"currentColor",height:"20",width:"20",viewBox:"0 0 40 40",className:(0,s.Z)(c,t),"aria-hidden":"true"},a),r.createElement("g",null,r.createElement("path",{d:"m34.5 11.7l-3 3.1-6.3-6.3 3.1-3q0.5-0.5 1.2-0.5t1.1 0.5l3.9 3.9q0.5 0.4 0.5 1.1t-0.5 1.2z m-29.5 17.1l18.4-18.5 6.3 6.3-18.4 18.4h-6.3v-6.2z"})))};var m=a(941);function i(e){let{editUrl:t}=e;return r.createElement("a",{href:t,target:"_blank",rel:"noreferrer noopener",className:m.kM.common.editThisPage},r.createElement(o,null),r.createElement(n.Z,{id:"theme.common.editThisPage",description:"The link label to edit the current page"},"Edit this page"))}},571:(e,t,a)=>{a.d(t,{r:()=>g,Z:()=>h});var r=a(7294),n=a(6010),l=a(941);function s(e){const t=e.getBoundingClientRect();return t.top===t.bottom?s(e.parentNode):t}function c(e){let{anchorTopOffset:t}=e;const a=Array.from(document.querySelectorAll(".anchor.anchor__h2, .anchor.anchor__h3")),r=a.find((e=>s(e).top>=t));if(r){return function(e){return e.top>0&&e.bottom<window.innerHeight/2}(s(r))?r:a[a.indexOf(r)-1]??null}return a[a.length-1]}function o(){const e=(0,r.useRef)(0),{navbar:{hideOnScroll:t}}=(0,l.LU)();return(0,r.useEffect)((()=>{e.current=t?0:document.querySelector(".navbar").clientHeight}),[t]),e}const m=function(e){const t=(0,r.useRef)(void 0),a=o();(0,r.useEffect)((()=>{const{linkClassName:r,linkActiveClassName:n}=e;function l(){const e=function(e){return Array.from(document.getElementsByClassName(e))}(r),l=c({anchorTopOffset:a.current}),s=e.find((e=>l&&l.id===function(e){return decodeURIComponent(e.href.substring(e.href.indexOf("#")+1))}(e)));e.forEach((e=>{!function(e,a){a?(t.current&&t.current!==e&&t.current?.classList.remove(n),e.classList.add(n),t.current=e):e.classList.remove(n)}(e,e===s)}))}return document.addEventListener("scroll",l),document.addEventListener("resize",l),l(),()=>{document.removeEventListener("scroll",l),document.removeEventListener("resize",l)}}),[e,a])},i="tableOfContents_vrFS",d="table-of-contents__link",u={linkClassName:d,linkActiveClassName:"table-of-contents__link--active"};function g(e){let{toc:t,isChild:a}=e;return t.length?r.createElement("ul",{className:a?"":"table-of-contents table-of-contents__left-border"},t.map((e=>r.createElement("li",{key:e.id},r.createElement("a",{href:`#${e.id}`,className:d,dangerouslySetInnerHTML:{__html:e.value}}),r.createElement(g,{isChild:!0,toc:e.children}))))):null}const h=function(e){let{toc:t}=e;return m(u),r.createElement("div",{className:(0,n.Z)(i,"thin-scrollbar")},r.createElement(g,{toc:t}))}},7211:(e,t,a)=>{a.d(t,{Z:()=>m});var r=a(7294),n=a(6010),l=a(6742);const s="tag_WK-t",c="tagRegular_LXbV",o="tagWithCount_S5Zl";const m=function(e){const{permalink:t,name:a,count:m}=e;return r.createElement(l.Z,{href:t,className:(0,n.Z)(s,{[c]:!m,[o]:m})},a,m&&r.createElement("span",null,m))}},7682:(e,t,a)=>{a.d(t,{Z:()=>m});var r=a(7294),n=a(6010),l=a(4973),s=a(7211);const c="tags_NBRY",o="tag_F03v";function m(e){let{tags:t}=e;return r.createElement(r.Fragment,null,r.createElement("b",null,r.createElement(l.Z,{id:"theme.tags.tagsListLabel",description:"The label alongside a tag list"},"Tags:")),r.createElement("ul",{className:(0,n.Z)(c,"padding--none","margin-left--sm")},t.map((e=>{let{label:t,permalink:a}=e;return r.createElement("li",{key:a,className:o},r.createElement(s.Z,{name:t,permalink:a}))}))))}}}]);