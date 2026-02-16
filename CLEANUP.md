# Cleanup Script - Remove Temporary Test Files

## Files to Remove

### Test Output Files (Safe to Delete)
- `assignment_test_results.txt`
- `driver_test_results.txt`
- `stats_test_results.txt`
- `stats_test_results_2.txt`
- `final_test_run.txt`
- `final_test_run_clean.txt`
- `last_test_output.txt`
- `test_output.txt`
- `last_run.txt`
- `last_run_3.txt`
- `last_run_4.txt`
- `last_run_final.txt`
- `last_run_final_2.txt`
- `last_run_final_3.txt`

### Build/Coverage Reports (Safe to Delete)
- `build_log.txt`
- `coverage.txt`
- `coverage_report.txt`
- `coverage_report_final.txt`
- `coverage_report_final_2.txt`
- `frontend_build.txt`
- `server_log.txt`
- `.coverage` (pytest coverage data)

### Verification Scripts (Can Keep or Delete)
- `manual_verify.py` - Manual verification script
- `verify_conn.py` - Database connection test

### Directories to Clean
- `.pytest_cache/` - Pytest cache (auto-regenerated)

## Cleanup Commands

```powershell
# Remove all test output files
Remove-Item assignment_test_results.txt, driver_test_results.txt, stats_test_results.txt, stats_test_results_2.txt, final_test_run.txt, final_test_run_clean.txt, last_test_output.txt, test_output.txt, last_run*.txt -ErrorAction SilentlyContinue

# Remove build/coverage reports
Remove-Item build_log.txt, coverage*.txt, frontend_build.txt, server_log.txt, .coverage -ErrorAction SilentlyContinue

# Remove pytest cache
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue

# Optional: Remove verification scripts
# Remove-Item manual_verify.py, verify_conn.py -ErrorAction SilentlyContinue
```

## Files to KEEP
- `README.md`
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `requirements.txt`
- `skillAdherenceRprt.md`
- All directories: `src/`, `tests/`, `frontend/`, `specs/`, `skills/`, `contracts/`, `interviews/`
