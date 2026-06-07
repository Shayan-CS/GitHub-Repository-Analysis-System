package com.githubanalysis.controller;

import com.githubanalysis.model.AnalysisEntity;
import com.githubanalysis.model.RepositoryEntity;
import com.githubanalysis.service.RepositoryService;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.List;
import java.util.Map;

@Controller
public class RepositoryController {
    private final RepositoryService service;

    public RepositoryController(RepositoryService service) {
        this.service = service;
    }

    @QueryMapping
    public RepositoryEntity getRepository(@Argument String id) {
        return service.getRepository(id).orElse(null);
    }

    @QueryMapping
    public List<RepositoryEntity> listRepositories(@Argument String language, @Argument Integer limit) {
        return service.listRepositories(language, limit);
    }

    @QueryMapping
    public AnalysisEntity getAnalysis(@Argument String repositoryId) {
        return service.getAnalysis(repositoryId).orElse(null);
    }

    @MutationMapping
    public Map addRepository(@Argument String githubUrl) {
        return service.addRepository(Map.of("github_url", githubUrl));
    }

    @MutationMapping
    public Map triggerAnalysis(@Argument String repositoryId) {
        return service.triggerAnalysis(repositoryId);
    }
}
