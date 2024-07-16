"use strict";(self.webpackChunksirji_docs=self.webpackChunksirji_docs||[]).push([[171],{9912:(i,e,s)=>{s.r(e),s.d(e,{assets:()=>d,contentTitle:()=>n,default:()=>u,frontMatter:()=>o,metadata:()=>c,toc:()=>l});var t=s(4848),r=s(8453);const o={sidebar_position:6},n="Sirji Studio",c={id:"custom-agents/sirji-studio",title:"Sirji Studio",description:"What is Sirji Studio?",source:"@site/docs/custom-agents/sirji-studio.md",sourceDirName:"custom-agents",slug:"/custom-agents/sirji-studio",permalink:"/custom-agents/sirji-studio",draft:!1,unlisted:!1,tags:[],version:"current",sidebarPosition:6,frontMatter:{sidebar_position:6},sidebar:"tutorialSidebar",previous:{title:"Agent Creation Steps",permalink:"/custom-agents/agent-creation-steps"},next:{title:"Architecture",permalink:"/architecture"}},d={},l=[{value:"What is Sirji Studio?",id:"what-is-sirji-studio",level:2},{value:"Why Use a GitHub Repository for Sirji Studio?",id:"why-use-a-github-repository-for-sirji-studio",level:2},{value:"Creating Sirji Studio from Scratch",id:"creating-sirji-studio-from-scratch",level:2},{value:"Configuring Sirji to Use Sirji Studio",id:"configuring-sirji-to-use-sirji-studio",level:2}];function a(i){const e={a:"a",code:"code",h1:"h1",h2:"h2",li:"li",ol:"ol",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,r.R)(),...i.components};return(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(e.h1,{id:"sirji-studio",children:"Sirji Studio"}),"\n",(0,t.jsx)(e.h2,{id:"what-is-sirji-studio",children:"What is Sirji Studio?"}),"\n",(0,t.jsx)(e.p,{children:"Sirji Studio is a collection of your custom agents and recipes, organized in a specific folder structure. We recommend storing these agents and recipes in a GitHub repository."}),"\n",(0,t.jsx)(e.h2,{id:"why-use-a-github-repository-for-sirji-studio",children:"Why Use a GitHub Repository for Sirji Studio?"}),"\n",(0,t.jsx)(e.p,{children:"A GitHub repository provides version control for your custom agents and recipes, making sharing them with your team members easier. Moreover, it helps with modifying and updating them as project conventions change."}),"\n",(0,t.jsx)(e.h2,{id:"creating-sirji-studio-from-scratch",children:"Creating Sirji Studio from Scratch"}),"\n",(0,t.jsx)(e.p,{children:"To set up Sirji Studio, follow these steps:"}),"\n",(0,t.jsxs)(e.ol,{children:["\n",(0,t.jsxs)(e.li,{children:[(0,t.jsx)(e.strong,{children:"Create Folders"}),": At the root level of the ",(0,t.jsx)(e.code,{children:"studio"})," folder, create ",(0,t.jsx)(e.code,{children:"recipes"})," and ",(0,t.jsx)(e.code,{children:"agents"})," folders."]}),"\n",(0,t.jsxs)(e.li,{children:[(0,t.jsx)(e.strong,{children:"Copy Configuration Files"}),": Copy these files to the ",(0,t.jsx)(e.code,{children:"agents"})," folder:","\n",(0,t.jsxs)(e.ul,{children:["\n",(0,t.jsx)(e.li,{children:(0,t.jsx)(e.a,{href:"https://github.com/sirji-ai/sirji/blob/main/sirji/vscode-extension/src/defaults/agents/ORCHESTRATOR.yml",children:"ORCHESTRATOR.yml"})}),"\n",(0,t.jsx)(e.li,{children:(0,t.jsx)(e.a,{href:"https://github.com/sirji-ai/sirji/blob/main/sirji/vscode-extension/src/defaults/agents/RECIPE_SELECTOR.yml",children:"RECIPE_SELECTOR.yml"})}),"\n",(0,t.jsx)(e.li,{children:(0,t.jsx)(e.a,{href:"https://github.com/sirji-ai/sirji/blob/main/sirji/vscode-extension/src/defaults/agents/RESEARCHER.yml",children:"RESEARCHER.yml"})}),"\n"]}),"\n"]}),"\n",(0,t.jsxs)(e.li,{children:["Follow the steps for agent creation from ",(0,t.jsx)(e.a,{href:"./agent-creation-steps",children:"here"}),"."]}),"\n",(0,t.jsxs)(e.li,{children:[(0,t.jsx)(e.strong,{children:"Commit to GitHub Repository (Optional)"}),": It is optional but recommended to commit the ",(0,t.jsx)(e.code,{children:"agents"})," and ",(0,t.jsx)(e.code,{children:"recipes"})," folders and all their files to a GitHub repository for version control."]}),"\n"]}),"\n",(0,t.jsx)(e.h2,{id:"configuring-sirji-to-use-sirji-studio",children:"Configuring Sirji to Use Sirji Studio"}),"\n",(0,t.jsx)(e.p,{children:"To configure Sirji to use your custom agents and recipes from a GitHub repository, follow these steps:"}),"\n",(0,t.jsxs)(e.ol,{children:["\n",(0,t.jsx)(e.li,{children:'After clicking the Sirji extension icon from the Activity Bar, click the "Open Sirji Studio" button.'}),"\n",(0,t.jsx)(e.li,{children:"In the opened VS Code window, open a terminal."}),"\n",(0,t.jsxs)(e.li,{children:['Remove the contents of the "studio" folder.',"\n",(0,t.jsx)(e.pre,{children:(0,t.jsx)(e.code,{className:"language-zsh",children:"rm -rf studio && mkdir studio\n"})}),"\n"]}),"\n",(0,t.jsxs)(e.li,{children:['Bring your custom agents and recipes to the "studio" folder:',"\n",(0,t.jsxs)(e.ul,{children:["\n",(0,t.jsxs)(e.li,{children:[(0,t.jsx)(e.strong,{children:"From your GitHub Repository"}),': Clone your GitHub repository into the "studio" folder:',"\n",(0,t.jsx)(e.pre,{children:(0,t.jsx)(e.code,{className:"language-zsh",children:"cd studio && git clone <repo URL> . && cd ..\n"})}),"\n"]}),"\n",(0,t.jsxs)(e.li,{children:[(0,t.jsx)(e.strong,{children:"Without version control"}),": Manually copy the ",(0,t.jsx)(e.code,{children:"agents"})," and ",(0,t.jsx)(e.code,{children:"recipes"}),' folders into the "studio" folder.']}),"\n"]}),"\n"]}),"\n"]})]})}function u(i={}){const{wrapper:e}={...(0,r.R)(),...i.components};return e?(0,t.jsx)(e,{...i,children:(0,t.jsx)(a,{...i})}):a(i)}},8453:(i,e,s)=>{s.d(e,{R:()=>n,x:()=>c});var t=s(6540);const r={},o=t.createContext(r);function n(i){const e=t.useContext(o);return t.useMemo((function(){return"function"==typeof i?i(e):{...e,...i}}),[e,i])}function c(i){let e;return e=i.disableParentContext?"function"==typeof i.components?i.components(r):i.components||r:n(i.components),t.createElement(o.Provider,{value:e},i.children)}}}]);