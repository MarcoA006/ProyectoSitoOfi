	function Password(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function General(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzáéíóú ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ()#0123456789-+/\(),.:";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
		
	function Letras(letra){
		var data = "abcdefghijklmnñopqrstuvwxyz ABCDEFGHIJKLMNÑOPQRSTUVWXYZ-+()._";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function LetrasAcento(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzáéíóú ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ-+()._";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function EmpresaCaracteresNumeros( letra )
	  {
		  var data = "abcdefghijklmnñopqrstuvwxyzáéíóú ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ-_()'.,1234567890&#!¡\/*[]~";
		  var nav4 = window.Event ? true : false;
		  var key = nav4 ? letra.which : letra.keyCode;
		
		  if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		  else
			return false;
	  }
	  
	  
	function Empresa(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzáéíóú ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ-()'.,_";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function EmpresaGeneral(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzáéíóú ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ-_()'.,1234567890";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function LetrasNumeros(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function LetrasNumerosEspacio(letra){
		var data = "abcdefghijklmnñopqrstuvwxyz ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function LetrasNumerosEspacioAcento(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzáéíóú ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ0123456789,";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function Direccion(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzáéíóú ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ()#0123456789.-";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
		
	function NumeroDomicilio(letra){
		var data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/- ";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function Busqueda(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzáéíóú ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ()#0123456789";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function Numeros(numero){
		var data = "0123456789";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? numero.which : numero.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function Moneda(numero){
		var data = "0.123456789";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? numero.which : numero.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function RFC(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ-0123456789";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function CURP(letra){
		var data = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function Telefono(numero){
		var data = "0123456789";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? numero.which : numero.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function Fecha(numero){
		var data = "0123456789-";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? numero.which : numero.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}

	function Mail(letra){
		var data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789@-.";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
	
	function Web(letra){
		var data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-~$+=,&.1234567890/:_";
		var nav4 = window.Event ? true : false;
		var key = nav4 ? letra.which : letra.keyCode;
		
		if (data.indexOf(String.fromCharCode(key)) > -1 || key <= 12)
			return true;
		else
			return false;
	}
			
	function findObj(n, d){
		var p, i ,x;
		
		if (!d) 
			d = document;
		
		if ((p = n.indexOf("?")) > 0 && parent.frames.length ){
			d = parent.frames[n.substring(p+1)].document;
			n = n.substring(0,p);
		}
		
		if (!(x = d[n]) && d.all)
			x = d.all[n];
		
		for (i=0; !x && i < d.forms.length; i++) 
			x = d.forms[i][n];
				
		for (i=0; !x && d.layers && i < d.layers.length; i++) 
			x = findObj(n, d.layers[i].document);
		
		return x;
	}

	function lTrim(Cadena){
		while (Cadena.charAt(0) == " ") 
			Cadena = Cadena.substr(1, Cadena.length - 1);		
		return Cadena;
	}
	
	function rTrim(Cadena){
		while (Cadena.charAt(Cadena.length - 1) == " ") 
			Cadena = Cadena.substr(0, Cadena.length - 1);	
		return Cadena;
	}

	function Trim(Cadena){
		return rTrim(lTrim(Cadena));
	}
	
	function Enfocar(name){
		var control = findObj(name);
		control.focus();
	}
	
	function Validar_Mail(_email) 
	{
     	var emailReg = /^[a-z][a-z-_0-9\.]+@[a-z-_=>0-9\.]+\.[a-z]{2,3}$/i
     	return emailReg.test(_email);
  	}
