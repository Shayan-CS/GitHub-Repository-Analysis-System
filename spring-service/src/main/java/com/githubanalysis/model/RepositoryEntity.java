package com.githubanalysis.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.OffsetDateTime;

@Entity
@Table(name = "repositories")
public class RepositoryEntity {
    @Id
    @Column(length = 36)
    private String id;

    @Column(name = "github_url")
    private String githubUrl;

    private String name;

    private String description;

    private Integer stars;

    private String language;

    private OffsetDateTime lastAnalyzed;

    private OffsetDateTime createdAt;

    public RepositoryEntity() {
    }

    // getters and setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getGithubUrl() {
        return githubUrl;
    }

    public void setGithubUrl(String githubUrl) {
        this.githubUrl = githubUrl;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Integer getStars() {
        return stars;
    }

    public void setStars(Integer stars) {
        this.stars = stars;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    public OffsetDateTime getLastAnalyzed() {
        return lastAnalyzed;
    }

    public void setLastAnalyzed(OffsetDateTime lastAnalyzed) {
        this.lastAnalyzed = lastAnalyzed;
    }

    public OffsetDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(OffsetDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
