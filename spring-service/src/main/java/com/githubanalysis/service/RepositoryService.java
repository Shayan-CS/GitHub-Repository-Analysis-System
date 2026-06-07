package com.githubanalysis.service;

import com.githubanalysis.client.FastApiClient;
import com.githubanalysis.model.AnalysisEntity;
import com.githubanalysis.model.RepositoryEntity;
import com.githubanalysis.repository.AnalysisRepository;
import com.githubanalysis.repository.RepositoryRepository;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class RepositoryService {
    private final RepositoryRepository repositoryRepository;
    private final AnalysisRepository analysisRepository;
    private final FastApiClient fastApiClient;

    public RepositoryService(RepositoryRepository repositoryRepository, AnalysisRepository analysisRepository,
            FastApiClient fastApiClient) {
        this.repositoryRepository = repositoryRepository;
        this.analysisRepository = analysisRepository;
        this.fastApiClient = fastApiClient;
    }

    public Optional<RepositoryEntity> getRepository(String id) {
        return repositoryRepository.findById(id);
    }

    public List<RepositoryEntity> listRepositories(String language, Integer limit) {
        if (language != null) {
            return repositoryRepository.findByLanguage(language);
        }
        return repositoryRepository.findAll().stream().limit(limit == null ? 100 : limit).toList();
    }

    public Optional<AnalysisEntity> getAnalysis(String repositoryId) {
        return analysisRepository.findByRepositoryId(repositoryId);
    }

    public Map addRepository(Map<String, Object> payload) {
        return fastApiClient.addRepository(payload).block();
    }

    public Map triggerAnalysis(String repositoryId) {
        return fastApiClient.triggerAnalysis(repositoryId).block();
    }
}
