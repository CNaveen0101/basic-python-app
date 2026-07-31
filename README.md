FROM eclipse-temurin:17-jre-noble
WORKDIR /app
COPY /target/narayani-market-1.0.0.jar .
EXPOSE 8080
CMD ["java", "-jar", "narayani-market-1.0.0.jar"]
