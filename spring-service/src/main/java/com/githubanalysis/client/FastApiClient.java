package com.githubanalysis.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import reactor.core.publisher.Mono;

import java.util.Map;

@Component
public class FastApiClient {
    private final WebClient webClient;

    public FastApiClient(@Value("${fastapi.base-url}") String baseUrl) {
        this.webClient = WebClient.builder().baseUrl(baseUrl).build();
    }

    public Mono<Map> addRepository(Map<String, Object> payload) {
        return webClient.post()
                .uri("/api/repositories")
                .contentType(MediaType.APPLICATION_JSON)
                .body(BodyInserters.fromValue(payload))
                .retrieve()
                .bodyToMono(Map.class);
    }

    public Mono<Map> triggerAnalysis(String repositoryId) {
        return webClient.post()
                .uri(uriBuilder -> uriBuilder.path("/api/analyze/{id}").build(repositoryId))
                .retrieve()
                .bodyToMono(Map.class);
    }
}
