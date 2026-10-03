import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import start_server; start_server()   # sert l'index.html et le dossier vendor/ du dépôt
from playwright.sync_api import sync_playwright
STUB = r"""
Object.defineProperty(Notification,'permission',{value:'default',writable:true,configurable:true});
window.supabase={createClient:()=>{
 const shop={id:'shop1',shop_name:'Boutique Audit',slug:'audit-shop',wa:'2250700000000',currency:'FCFA',expiry:'2026-12-01',blocked:false,appearance:{},anns:[]};
 const D={shops:[shop],
  products:[{id:'r1',owner_id:'shop1',data:{id:'p1',name:'Pagne',newP:12000,oldP:15000,qty:5,qtyAvail:5,imgs:[],vars:['S','M'],desc:'Tissu',slug:'pagne',date:'01/10/2026'}}],
  orders:[{id:'o1',owner_id:'shop1',data:{id:'o1',prodName:'Pagne',prenom:'Awa',ville:'Ouaga',qrt:'Z1',tel:'70',total:12000,qty:1,newP:12000,date:'01/10/2026',status:'attente'}}]};
 const mk=t=>{const c={eq(){return c},neq(){return c},order(){return c},in(){return c},gte(){return c},lte(){return c},ilike(){return c},or(){return c},range(){return c},
   limit:()=>Promise.resolve({data:D[t]||[],error:null}),maybeSingle:async()=>({data:t==='shops'?shop:null,error:null}),single:async()=>({data:t==='shops'?shop:null,error:null}),
   then:(r)=>r({data:D[t]||[],error:null}),delete(){return c},update(){return c}};return c;};
 const ch={on(){return ch},subscribe(){return ch}};
 return{auth:{signUp:async()=>({data:{user:{id:'shop1'},session:null},error:null}),signInWithPassword:async()=>({data:{user:{id:'shop1'}},error:null}),
   signOut:async()=>({error:null}),getSession:async()=>({data:{session:null},error:null}),onAuthStateChange:()=>({data:{subscription:{unsubscribe(){}}}})},
  from:t=>({select:()=>mk(t),insert:async()=>({data:null,error:null}),update:()=>mk(t),delete:()=>mk(t),upsert:async()=>({data:null,error:null})}),
  rpc:async n=>(/get_|_list|conversations|messages|orders|concerns|gerants|marketplace/.test(n)?{data:[],error:null}:{data:{success:true},error:null}),
  storage:{from:()=>({upload:async()=>({data:{path:'x'},error:null}),getPublicUrl:()=>({data:{publicUrl:''}})})},
  channel:()=>ch,removeChannel(){},functions:{invoke:async()=>({data:null,error:null})}};
}};
"""
MERCHANT=['p-overview','p-boutique','p-appearance','p-produits','p-promos','p-messages','p-wallet','p-livraison','p-commandes','p-clients-shop','p-stock','p-stats','p-gerant','p-livreurs','p-abo','p-gerant-notifs','p-aide']
ADMIN=['adm-abos','adm-annonces','adm-clients','adm-empreinte','adm-escrow','adm-messages','adm-profil','adm-reports','adm-reviews','adm-stats','adm-support','adm-youtube']
SCREENS=['s-land','s-about','s-privacy','s-login','s-register','s-admin-login','s-gerant-login','s-livreur-login','s-marketplace','s-client-orders','s-client-favorites','s-client-messages']
LOGIN="await loginAs({id:'shop1',name:'M',shopName:'Boutique Audit',email:'t@t.com',wa:'07',isAdmin:false,isGerant:false,blocked:false,expiry:'01/12/2026'});"
def groups():
  G=[]
  G.append(('Écrans publics',[(f'Écran {s}', f"go('{s}')") for s in SCREENS]+[
    ('Popup inscription client','showClientRegisterPopup()'),('Popup connexion client','document.querySelectorAll(".overlay").forEach(o=>o.remove()); showClientLoginPopup()'),
    ('Invitations notifications (x3)','maybePromptPushNotifications(); maybePromptLivreurPushNotifications(); maybePromptClientPushNotifications();')]))
  G.append(('Espace marchand',[('Connexion marchand',LOGIN)]+[(f'Section {m}', f"pg('{m}', document.querySelector(`.nav-item[onclick*=\"'{m}'\"]`))") for m in MERCHANT]+[
    ('Formulaire ajout produit','showAddForm(); addSection("title"); addSection("space");'),
    ('Enregistrer un produit',"pg('p-produits',null); showAddForm(); const n=document.getElementById('pf-name'); if(n) n.value='Test'; const pr=document.getElementById('pf-new')||document.getElementById('pf-price'); if(pr) pr.value='5000'; await saveProduct();"),
    ('Tarif de livraison',"const w=document.createElement('div'); w.innerHTML='<input id=dz-sector value=Ouaga><input id=dz-price value=500><input id=dz-free type=checkbox>'; document.body.appendChild(w); await saveDeliveryZone();"),
    ('Activer/supprimer une offre',"await togglePromoActive('x',true); await deletePromoOffer('x');"),
    ('Valider une commande',"S.orders=[{id:'o1',_rowId:'r',prodName:'P',ville:'O',total:1,qty:1,newP:1,date:'01/10/2026',prenom:'A',tel:'7',qrt:'Z'}]; await valCmd('o1');"),
    ('Annuler une commande',"S.orders=[{id:'o2',_rowId:'r2',prodName:'P',ville:'O',total:1,qty:1,newP:1,date:'01/10/2026',prenom:'A',tel:'7',qrt:'Z'}]; await annCmd('o2');"),
    ('Assigner un livreur',"S.orders=[{id:'o3',_rowId:'r3',prodName:'P',ville:'O',total:1,qty:1,newP:1,date:'01/10/2026',prenom:'A',tel:'7',qrt:'Z'}]; S.livreurs=[{id:'lv1',name:'K',phone:'7',email:'k@k.com'}]; openAssignLivreur('o3'); document.querySelector('[data-lvid=\"lv1\"]')?.click();"),
    ('Statistiques + graphique',"pg('p-stats',null); renderStats && renderStats(); const c=document.createElement('canvas'); c.id='zz'; document.body.appendChild(c); drawLineChart('zz',['a'],[1],'#1A56E8');"),
    ('Apparence',"pg('p-appearance',null); await saveAppearance();"),
    ('Journal gérant',"pg('p-gerant',null); await showGerantActivity('g1','g@g.com');"),
    ('Déconnexion','await logout();')]))
  G.append(('Espace gérant',[('Connexion gérant',"S.gerantRecordId='g1'; await loginAs({id:'shop1',ownerId:'shop1',name:'G',shopName:'B',email:'g@g.com',wa:'07',isAdmin:false,isGerant:true,blocked:false,expiry:'01/12/2026'});")]+
    [(f'Section {m}', f"pg('{m}', document.querySelector(`.nav-item[onclick*=\"'{m}'\"]`))") for m in ['p-produits','p-commandes','p-clients-shop']]))
  G.append(('Espace admin',[('Écran admin',"go('s-admin')")]+[(f'Section {a}', f"admPg('{a}', document.querySelector(`[onclick*=\"'{a}'\"]`))") for a in ADMIN]+[('Publier annonce (vide → contrôle)','await publishAnnouncement();')]))
  G.append(('Espace livreur',[('Tableau de bord livreur',"S.livreurSession={livreurId:'lv1',phone:'7',code:'1',name:'K',shopName:'B',currency:'FCFA'}; showLivreurDash();")]))
  G.append(('Boutique publique',[('Lien de boutique /b/audit-shop',"await openPublicShopBySlug({type:'shop',shopSlug:'audit-shop',page:'home'});"),
    ('Catalogue','renderPublicCatalogue();'),
    ('Fiche produit',"S.products=[{id:'p1',name:'Pagne',oldP:15000,newP:12000,qty:5,qtyAvail:5,imgs:[],vars:['S'],desc:'d',date:'01/10/2026'}]; previewShop('p1',true);"),
    ('Quantité + total','chQty(1); updTotal();'),('Note avis','setProdReviewStars(5);'),('Signaler marchand','showReportMerchantPopup();'),
    ('Chat client',"document.querySelectorAll('.overlay:not([id])').forEach(o=>o.remove()); S.client={id:'c1',name:'A',email:'a@a.com'}; S.curProd={id:'p1',name:'Pagne'}; await openChatWithMerchant(); closeChatOverlay();"),
    ('Zyn Assurance','showCreateEscrowForm();'),
    ('Passer commande',"previewShop('p1',true); document.getElementById('or-prenom').value='Awa'; document.getElementById('or-ville').value='Ouaga'; document.getElementById('or-qrt').value='Z1'; document.getElementById('or-tel-num').value='70123456'; await submitOrder();")]))
  return G
DEVICES=[('Android 390px',dict(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=2)),
 ('Petit Android 360px',dict(viewport={'width':360,'height':740},is_mobile=True,has_touch=True,device_scale_factor=2)),
 ('iPhone (simulé)',dict(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=3,user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')),
 ('Ordinateur 1366px',dict(viewport={'width':1366,'height':768}))]
total=0; fails=[]
with sync_playwright() as p:
  b=p.chromium.launch()
  for dname,dopts in DEVICES:
    dpass=0; dtot=0
    for gname,steps in groups():
      ctx=b.new_context(**dopts); pg_=ctx.new_page(); pg_.add_init_script(STUB)
      pg_.route('**/*',lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') else r.abort())
      errs=[]; pg_.on('pageerror',lambda e: errs.append(str(e).split('\n')[0][:110]))
      pg_.on('dialog', lambda d: d.accept())
      pg_.goto('http://127.0.0.1:8765/',wait_until='domcontentloaded'); pg_.wait_for_timeout(1200)
      for sname,code in steps:
        before=len(errs); res=None
        try: pg_.evaluate("async()=>{"+code+"}"); pg_.wait_for_timeout(250)
        except Exception as e: res=str(e).split('\n')[0][:110]
        new=errs[before:]; ok=(res is None and not new); dtot+=1; dpass+=ok
        if not ok: fails.append((dname,gname,sname,res,new))
      ctx.close()
    total+=dtot; print(f"{dname:<20} : {dpass}/{dtot} tests réussis")
  b.close()
print(f"\nTOTAL : {total-len(fails)}/{total}")
for f in fails: print("❌",f)
# Résumé lisible dans l'onglet GitHub Actions
summary = os.environ.get('GITHUB_STEP_SUMMARY')
if summary:
  with open(summary, 'a', encoding='utf-8') as fh:
    fh.write(f"## Tests Zyntelo : {total-len(fails)}/{total} réussis\n\n")
    fh.write("✅ Aucune régression détectée.\n" if not fails else "".join(f"- ❌ **{d}** · {g} · {n} : {r or ''} {e}\n" for d,g,n,r,e in fails))
# Code de sortie : la CI échoue automatiquement si un seul test échoue
sys.exit(1 if fails or total != 288 else 0)
