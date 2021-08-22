CREATE TABLE job_defs (
    id SERIAL PRIMARY KEY,
    job_link VARCHAR(512) NUT NULL
);

CREATE TABLE job_runs (
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL,
    job_run_id INTEGER NOT NULL,
    params JSONB,
    display_name VARCHAR(512),
    full_job_url VARCHAR(512) NOT NULL,
    job_causer JSONB NOT NULL,
    job_duration INTEGER NOT NULL,
    job_timestamp BIGINT NOT NULL,
    job_result VARCHAR(24),
    job_timings JSONB,
    job_git_dets JSONB,
    FOREIGN KEY (job_id) REFERENCES job_defers(id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    UNIQUE (job_id, job_run_id)
);

