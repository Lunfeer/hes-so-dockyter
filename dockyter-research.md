# Dockyter – Research & Alignment Notes

## 1. Project goal & target audience

### 1.1 Goal

Dockyter is an **IPython extension** that adds a `%%docker` magic and optional `!` redirection so that:

- users can run **CLI tools packaged as Docker images** from inside notebooks,
- while keeping the **base Python environment light** (no need to install every tool into the kernel image).

This follows the same pattern as existing extensions like `ipython-sql`, which add `%sql` / `%%sql` magics as a separate PyPI package rather than being integrated into IPython core.   

### 1.2 Target users

Dockyter is primarily aimed at:

1. **Data scientists / data engineers**  
   - who already use Docker to package tools (ML training CLIs, data validators, bioinformatics pipelines, etc.),  
   - and want to call these tools from notebooks without polluting the main environment.

2. **JupyterHub / Binder operators**  
   - who want to keep their **notebook images small** but still allow some teams to run heavy tools in sidecar containers,  
   - and who can explicitly choose to expose a container runtime (Docker/Podman) in certain profiles only.   

3. **Teams working with Databricks / similar platforms (local dev side)**  
   - Many Databricks users work locally in **VS Code or Jupyter** and connect to Databricks clusters via Databricks Connect, often using Docker dev containers.   
   - Dockyter is useful in these **local Jupyter environments** to orchestrate Dockerised tools around the code that talks to Databricks (testing, preprocessing, validation, etc.).

Dockyter is **not** primarily targeted at running directly inside **managed Databricks notebooks** (where users typically don’t have direct access to the Docker daemon of the cluster), but rather at the broader Jupyter ecosystem where the user or admin controls the environment.

---

## 2. Conventional Commits

For this project we follow the **Conventional Commits 1.0.0** specification:   

Basic format:

```text
<type>[optional scope]: <description>
```

Examples relevant to Dockyter:

* `feat(dockyter): add initial %%docker magic prototype`
* `fix(docker-magic): handle missing docker CLI with clear error`
* `docs: document architecture and security trade-offs`
* `test(dockyter): add tests for docker argument parsing`

This improves commit history readability and makes future tooling (changelogs, release notes) easier.

---

## 3. Docker inside Binder / JupyterHub

### 3.1 How Binder normally uses Docker

* **BinderHub** uses **repo2docker** to build Docker images from repositories, typically by talking to a Docker or compatible socket (`/var/run/docker.sock`) or a Docker-in-Docker / Podman setup.
* These builds happen in **dedicated build pods**, not inside the user’s notebook container.

### 3.2 Why “docker inside user notebooks” is tricky

For public Binder / mybinder.org style deployments, cluster operators are **very cautious** about:

* mounting the Docker socket into user containers,
* or letting users run arbitrary `docker run` from notebooks.

This is considered risky because access to the Docker socket can give almost full control over the host / cluster.

**Implication for Dockyter:**

* On **public Binder / shared JupyterHub**, Dockyter will usually **not** be enabled, unless an admin has explicitly decided to expose a container runtime in a controlled way.
* Dockyter is a better fit for:

  * **local Jupyter environments**, or
  * **private JupyterHub deployments** where admins design a secure setup (possibly using rootless Podman or dedicated sidecar runtimes).

---

## 4. IPython / Jupyter contribution guidelines

To eventually get Dockyter recognised in the IPython ecosystem (even as an external extension), it’s important to follow the existing **IPython / Jupyter contributing guidelines**:

* **IPython Development Guide**: overview of how IPython development works (GitHub workflow, code style, tests, etc.).
* **“The Perfect Pull Request”**: describes expectations for PRs:

  * the code does what it should,
  * works on the supported platforms,
  * includes tests and documentation,
  * is focused and reviewable.
* **General Jupyter contributing guide**: emphasises reading contribution docs, starting small, and using beginner-friendly issues as entry points.

For Dockyter-related contributions upstream (IPython), this means:

* keep PRs **small and generic** (e.g. adding hooks or improving docs),
* include **tests** and clear **documentation**,
* discuss design ideas early (Discourse / GitHub issues) before sending large PRs.

---

## 5. Strategy for Dockyter & IPython

Taking inspiration from `ipython-sql` and other IPython extensions that live on PyPI and integrate cleanly via `%load_ext`,  the plan is:

1. **Polish Dockyter as an IPython extension**

   * Clear API: `%load_ext dockyter`, `%%docker`, `%docker_off`, `%docker_status`.
   * Graceful behaviour if `docker` is not installed (helpful error, no crash).
   * Documentation + example notebooks:

     * basic usage,
     * example with Binder setup (built on top of JupyterHub),
     * optional example for teams using Databricks Connect or Kubeflow locally.

2. **Publish Dockyter on PyPI**

   * `pip install dockyter` works in a clean venv.
   * Add the classifier `Framework :: IPython` to signal it’s an IPython extension.

3. **Upstream visibility (IPython / Jupyter)**

   * Open a GitHub issue / PR to:

     * propose adding Dockyter to a “third-party magics / extensions” section in IPython docs,
   * Follow the IPython dev guidelines for PRs (tests, docs, small scope).

This path keeps Dockyter as an **opt-in extension** (like `%sql`) that can still be part of the “IPython ecosystem” and gives you a realistic way to become a recognised contributor (through PRs, docs, and small hooks upstream).