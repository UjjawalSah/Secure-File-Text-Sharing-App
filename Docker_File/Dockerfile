# Use the official Tomcat base image
FROM tomcat:9.0

# Copy the WAR file to the webapps directory in Tomcat
COPY ROOT.war /usr/local/tomcat/webapps/

# Expose port 8080
EXPOSE 8080

# Start Tomcat
CMD ["catalina.sh", "run"]
