# minecraft server ansible installer

**Minecraft Server Version**: 1.16.5

```bash
$ ansible-playbook -kK ./minecraft.yml -i ./inventory-minecraft.ini --user [user] --limit [host]
```

**OpenJDK**
For Windows, download the [OpenJDK zip](https://download.java.net/java/GA/jdk21.0.2/f2283984656d49d69e91c558476027ac/13/GPL/openjdk-21.0.2_windows-x64_bin.zip) and place it in `ansible/roles/win32nt/files/`.

**TODO**:
- better docs/instructions