package Backend;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.*;
import java.util.Arrays;

@WebServlet("/FileRetrieveServlet")
public class FileRetrieveServlet extends HttpServlet {
    private static final String UPLOAD_DIR = "uploads";
    private static final String TEXTS_DIR = "shared_texts";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String fileCode = request.getParameter("fileCode");

        // Check if it's a text code or file code
        if (isTextCode(fileCode)) {
            handleTextRetrieval(fileCode, response);
        } else {
            handleFileRetrieval(fileCode, response);
        }
    }

    private boolean isTextCode(String code) {
        // Determine if the code refers to a text file
        File textsDir = new File(getServletContext().getRealPath("") + File.separator + TEXTS_DIR);
        File[] textFiles = textsDir.listFiles((dir, name) -> name.equals(code + ".txt"));
        return textFiles != null && textFiles.length == 1;
    }

    private void handleTextRetrieval(String textCode, HttpServletResponse response) throws IOException {
        File textsDir = new File(getServletContext().getRealPath("") + File.separator + TEXTS_DIR);
        File[] textFiles = textsDir.listFiles((dir, name) -> name.equals(textCode + ".txt"));

        if (textFiles != null && textFiles.length == 1) {
            File textFile = textFiles[0];
            response.setContentType("text/plain");
            response.setContentLength((int) textFile.length());
            response.setHeader("Content-Disposition", "attachment; filename=\"" + textFile.getName() + "\"");

            try (BufferedReader reader = new BufferedReader(new FileReader(textFile))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    response.getWriter().println(line);
                }
            } catch (IOException e) {
                response.getWriter().println("Error reading text file: " + e.getMessage());
            }
        } else {
            response.getWriter().println("Text not found or invalid text code.");
        }
    }

    private void handleFileRetrieval(String fileCode, HttpServletResponse response) throws IOException {
        File uploadsDir = new File(getServletContext().getRealPath("") + File.separator + UPLOAD_DIR);
        File[] files = uploadsDir.listFiles((dir, name) -> name.startsWith(fileCode + "_"));

        if (files != null && files.length > 0) {
            File file = files[0];  // Assuming files[0] is the desired file; adjust logic if multiple files should be handled differently
            response.setContentType(getServletContext().getMimeType(file.getName()));
            response.setContentLength((int) file.length());
            response.setHeader("Content-Disposition", "attachment; filename=\"" + file.getName().substring(file.getName().indexOf('_') + 1) + "\"");

            try (FileInputStream in = new FileInputStream(file)) {
                byte[] buffer = new byte[1024];
                int bytesRead;
                while ((bytesRead = in.read(buffer)) != -1) {
                    response.getOutputStream().write(buffer, 0, bytesRead);
                }
            }
        } else {
            response.getWriter().println("File not found or invalid file code.");
        }
    }
}
