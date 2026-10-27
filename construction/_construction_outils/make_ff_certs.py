# Firefox 31.8 portable (pack 2) : racines de certification recentes + moteur
# DuckDuckGo Lite. Ecrit les sources texte dans src_stage\firefox\App\Firefox :
#   defaults\pref\autoconfig.js  -> active mozilla.cfg
#   mozilla.cfg                  -> ajoute les racines a chaque demarrage
#                                   (nsIX509CertDB.addCertFromBase64, confiance SSL)
#   browser\searchplugins\ddg-lite.xml -> moteur, a cote de Google, Bing...
# Usage : make_ff_certs.py <dossier certs (DER)> <icone .ico> <src_stage\firefox>
import base64
import sys
from pathlib import Path

CERTS, ICO, DST = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]) / "App" / "Firefox"
NOMS = {
    "DigiCertGlobalRootG2.crt": "DigiCert Global Root G2 (DuckDuckGo, Microsoft...)",
    "DigiCertGlobalRootG3.crt": "DigiCert Global Root G3",
    "isrgrootx1.der": "ISRG Root X1 (Let's Encrypt)",
    "isrg-root-x2.der": "ISRG Root X2 (Let's Encrypt)",
    "root-ye.der": "ISRG Root YE (Let's Encrypt, 2025)",
    "root-yr.der": "ISRG Root YR (Let's Encrypt, 2025)",
    "gtsr1.der": "GTS Root R1 (Google)",
    "gtsr4.der": "GTS Root R4 (Google)",
    "AmazonRootCA1.cer": "Amazon Root CA 1",
    "AmazonRootCA3.cer": "Amazon Root CA 3",
    "USERTrustRSA.crt": "USERTrust RSA (Sectigo)",
}

lignes = []
for f, nom in NOMS.items():
    der = (CERTS / f).read_bytes()
    assert der[0] == 0x30, f
    lignes.append('  // %s\n  "%s"' % (nom, base64.b64encode(der).decode()))

CFG = r'''// Pack Win98FR - Firefox 31.8 : configuration lue a chaque demarrage
// Racines de certification recentes, absentes de Firefox 31 (2015) : sans
// elles, DuckDuckGo et beaucoup de sites affichent "connexion non certifiee".
// Ajoutees au magasin du profil (cert8.db), confiance "sites web" seulement.
// Le magasin n'est pret qu'apres le choix du profil : ajout a "final-ui-startup",
// avant l'ouverture de la premiere fenetre.
var racines = [
@RACINES@
];
function ajouteRacines() {
  // Firefox 31 : addCertFromBase64 est dans nsIX509CertDB2 (fusionne plus tard)
  var Ci = Components.interfaces;
  var certdb = Components.classes["@mozilla.org/security/x509certdb;1"]
    .getService(Ci.nsIX509CertDB2 ? Ci.nsIX509CertDB2 : Ci.nsIX509CertDB);
  for (var i = 0; i < racines.length; i++) {
    try { certdb.addCertFromBase64(racines[i], "C,,", ""); } catch (e) {}
  }
}
try {
  Components.classes["@mozilla.org/observer-service;1"]
    .getService(Components.interfaces.nsIObserverService)
    .addObserver({ observe: function () { try { ajouteRacines(); } catch (e) {} } },
                 "final-ui-startup", false);
} catch (e) {}
'''
(DST / "mozilla.cfg").write_text(CFG.replace("@RACINES@", ",\n".join(lignes)), encoding="utf-8")

ac = DST / "defaults" / "pref" / "autoconfig.js"
ac.parent.mkdir(parents=True, exist_ok=True)
ac.write_text("// Pack Win98FR : lit mozilla.cfg (racines de certification recentes)\n"
              "pref(\"general.config.filename\", \"mozilla.cfg\");\n"
              "pref(\"general.config.obscure_value\", 0);\n", encoding="utf-8")

ico = base64.b64encode(ICO.read_bytes()).decode()
sp = DST / "browser" / "searchplugins" / "ddg-lite.xml"
sp.parent.mkdir(parents=True, exist_ok=True)
sp.write_text('<SearchPlugin xmlns="http://www.mozilla.org/2006/browser/search/">\n'
              '<ShortName>DuckDuckGo Lite</ShortName>\n'
              '<Description>DuckDuckGo, version legere</Description>\n'
              '<InputEncoding>UTF-8</InputEncoding>\n'
              '<Image width="16" height="16">data:image/x-icon;base64,%s</Image>\n'
              '<Url type="text/html" method="GET" template="https://lite.duckduckgo.com/lite/">\n'
              '  <Param name="q" value="{searchTerms}"/>\n'
              '</Url>\n'
              '<SearchForm>https://lite.duckduckgo.com/lite/</SearchForm>\n'
              '</SearchPlugin>\n' % ico, encoding="utf-8")
print("ok :", len(lignes), "racines")
