package com.githubanalysis.repository;

import com.githubanalysis.model.AnalysisEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface AnalysisRepository extends JpaRepository<AnalysisEntity, String> {
    Optional<AnalysisEntity> findByRepositoryId(String repositoryId);
}
