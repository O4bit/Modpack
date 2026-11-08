# Create Stellar — packwiz

Local packwiz conversion of **Create Stellar 2.0.2**, originally by **ellipog**,
for **Minecraft 1.21.1 / NeoForge 21.1.264**.

This pack is based on the working Prism snapshot, with pinned mods,
including Simple Voice Chat and subsequent additions. It includes
the pack's 765 configuration/quest/assets overrides, resource packs and shader.
Mod JARs are downloaded from their original Modrinth/CurseForge URLs.

This replaces the original Better Building pack while preserving Git history
and the repository remote.

## Install and keep clients updated

Use a Prism instance for Minecraft 1.21.1 with NeoForge 21.1.264 and a compatible
Java runtime (Minecraft/NeoForge require Java 21 or newer). Use the
[official packwiz-installer-bootstrap](https://github.com/packwiz/packwiz-installer-bootstrap/releases)
in the instance's Minecraft directory, then set Prism's pre-launch command to:

```sh
"$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://modpack.exo-serve.space/pack.toml
```

That URL serves this snapshot after the branch is merged/pushed and GitHub Pages
deploys. The custom domain is `modpack.exo-serve.space`. At the DNS provider,
configure `modpack` as a CNAME pointing to `o4bit.github.io`, replacing A/AAAA
records at that exact subdomain. The CNAME target has no protocol or repository
path. Keep the same custom domain in the repository's GitHub Pages settings.

Installing into a fresh instance is recommended when switching from Better
Building. This is a client pack; use the separate dedicated-server package for
hosting. Common mods are marked `both` based on the upstream server pack;
the remaining mods and resource packs are marked `client`.

Sodium is required. LambDynamicLights, Offhand Torch & Lantern Tweak, and
Sodium Extra are optional client mods, selected by default. Compatible updaters
such as unsup let players choose whether to install them.

For excessive anvil costs, Too Expensive Removed caps an item's accumulated
prior-work penalty at 25. Move the affected equipment and enchanted book into
your inventory using normal cursor clicks, then put them back in the anvil.
Shift-clicking does not trigger the correction. Normal enchantment charges
still apply, and the mod must also be installed on the multiplayer server.

## Maintain

Run commands from this repository:

```sh
./packwiz list
./packwiz refresh
python3 scripts/validate_pack.py
./packwiz serve
```

For local installer testing, use `http://localhost:8080/pack.toml` while
`packwiz serve` is running. Refresh and validate after changing any files.
Updating every mod independently can break the upstream pack's compatibility;
keep versions pinned until a change has been checked against the server.

The Pages workflow validates the index and stages only indexed pack files.
It does not publish the packwiz executable, scripts, Git internals, or personal
data. It deploys only on pushes to `main` or manual workflow dispatch.

## Scope and credits

The source is the local Prism instance's pinned metadata and original override
list for Create Stellar 2.0.2. Original pack authors and individual mod/resource
pack authors retain their respective rights. The existing repository license
does not replace third-party licenses.

Personal saves, screenshots, logs, server lists, authentication data, map
caches, and server bot configurations are not included. The private experimental
C2ME build and pregenerated server world are not part of this client pack.
Resource packs and shaders are supplied without overwriting player controls or
their personal `options.txt`.
