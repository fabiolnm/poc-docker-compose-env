# Docker Compose Environment Variable POC

Docker Compose's declarative model requires environment variables to be explicitly declared in the YAML file. There is no `-e` flag for `docker compose up` (unlike `docker compose run -e`).

## Demo

Demonstrates that `docker compose up` cannot pass environment variables to containers without explicitly declaring them in `docker-compose.yml`.

## Files

- `main.py` - Prints the value of `HELLO` env var
- `Dockerfile` - Simple Python container
- `docker-compose.yml` - Compose configuration

## Run the POC

### Test 1: No environment declaration

```yaml
# docker-compose.yml
services:
  hello:
    build: .
```

```bash
docker compose up
```

**Result:** `HELLO=NOT SET`

### Test 2: Shell env var without YAML declaration

```yaml
# docker-compose.yml (same as above)
services:
  hello:
    build: .
```

```bash
HELLO=WORLD docker compose up
```

**Result:** `HELLO=NOT SET`

The shell variable is ignored because it's not declared in the compose file.

### Test 3: Shell env var with YAML declaration

```yaml
# docker-compose.yml
services:
  hello:
    build: .
    environment:
      HELLO: ${HELLO}
```

```bash
HELLO=WORLD docker compose up
```

**Result:** `HELLO=WORLD`

## Summary

| Test | docker-compose.yml | Command | Container sees |
|------|-------------------|---------|----------------|
| 1 | No `environment` | `docker compose up` | `HELLO=NOT SET` |
| 2 | No `environment` | `HELLO=WORLD docker compose up` | `HELLO=NOT SET` |
| 3 | `HELLO: ${HELLO}` | `HELLO=WORLD docker compose up` | `HELLO=WORLD` |

## Alternative: `docker compose run -e`

Unlike `docker compose up`, the `run` command supports the `-e` flag:

```bash
docker compose run -e HELLO=WORLD hello
```

**Result:** `HELLO=WORLD`

This works because `run` starts a single container interactively, bypassing the declarative model.

## Conclusion

To pass env vars at runtime with `docker compose up`, you must declare them in:
1. `docker-compose.yml`
2. An override file (`docker-compose.override.yml`)
3. Stdin (`docker compose -f docker-compose.yml -f - up`)

For ad-hoc runs, use `docker compose run -e VAR=value service_name` instead.
