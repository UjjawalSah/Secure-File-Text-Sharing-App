package Backend;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

@WebServlet("/VisitorCounterServlet")
public class VisitorCounterServlet extends HttpServlet {
    private static final String COUNTER_FILE = "counter.txt";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Get the session associated with this request
        HttpSession session = request.getSession(true);

        // Check if the session attribute for visit tracking exists
        if (session.getAttribute("visited") == null) {
            // If the session attribute doesn't exist, this is the first visit
            // Increment the count and mark the session as visited
            incrementVisitorCount();
            session.setAttribute("visited", true);
        }

        // Get the current count from the counter file
        int count = getCurrentVisitorCount();

        // Respond with the current count
        response.setContentType("text/plain");
        response.getWriter().write(Integer.toString(count));
    }

    private synchronized void incrementVisitorCount() throws IOException {
        String filePath = getServletContext().getRealPath("/") + COUNTER_FILE;

        int count = getCurrentVisitorCount();
        count++;

        // Write the updated count to the file
        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write(Integer.toString(count));
        }
    }

    private int getCurrentVisitorCount() throws IOException {
        String filePath = getServletContext().getRealPath("/") + COUNTER_FILE;
        File counterFile = new File(filePath);

        if (!counterFile.exists()) {
            // If file doesn't exist, create it with initial count 0
            try (FileWriter writer = new FileWriter(counterFile)) {
                writer.write("0");
            }
            return 0;
        }

        try (FileReader reader = new FileReader(counterFile)) {
            StringBuilder sb = new StringBuilder();
            int character;
            while ((character = reader.read()) != -1) {
                sb.append((char) character);
            }
            return Integer.parseInt(sb.toString().trim());
        }
    }
}
