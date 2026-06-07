package com.githubanalysis.repository;

import com.githubanalysis.model.RepositoryEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RepositoryRepository extends JpaRepository<RepositoryEntity, String> {
    List<RepositoryEntity> findByLanguage(String language);
}
