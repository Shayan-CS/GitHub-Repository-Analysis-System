FROM eclipse-temurin:17-jdk-jammy
WORKDIR /app
COPY pom.xml ./
COPY src ./src
RUN ./mvnw -v || true
RUN apt-get update && apt-get install -y maven
RUN mvn -f pom.xml -DskipTests package
EXPOSE 8080
ENTRYPOINT ["java","-jar","target/spring-service-0.0.1-SNAPSHOT.jar"]
