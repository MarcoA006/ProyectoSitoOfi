function decodeTomcatStrings() {
    const p = "aRfguQwJvbc#h l)[W2jkm/op?N!rVisGq=@tB3O4CdeF9n0U(HI_6X]KLM>,DE.-Pxyz15YZ<78AST";
    const l = "gJvbUWc#,Dh5w*sGq=@tB[!39nO4CuYdeF0a]Kl)iQxZ<7yf2jkSTrVm/oR-Pp?NI_6XLM>E.z18A(H";
    
    function f(D) {
        var F = D.split("").reverse();
        var E = "";
        for(let cont = 0; cont < F.length; cont++) {
            for(let cont2 = 0; cont2 < l.length; cont2++) {
                if(l[cont2] == F[cont]) {
                    E = E + "" + p[cont2];
                    break;
                }
            }
        }
        return E;
    }
    
    // Strings importantes del backdoor
    const importantStrings = [
        ")HS(*39YUF?",
        "gYhCge*3y3H*Zd3#",
        "3]hZX3C_*Zx*CZxYo*PC3xgss3CCgdZp",
        "whygJ9(*I*9dsXyxa*I*-D!z9(*sZXygp-Dz*HQ(S*I*fMf@*]wbYCX93h"
    ];
    
    importantStrings.forEach(str => {
        console.log(`Original: ${str} -> Decoded: ${f(str)}`);
    });
}

decodeTomcatStrings();
