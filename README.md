# Ombi APT repo

```bash
curl -sSL https://roxedus.github.io/apt-test/pub.key | sudo apt-key add -
echo "deb https://roxedus.github.io/apt-test jessie develop" | tee /etc/apt/sources.list.d/ombi.list
```
