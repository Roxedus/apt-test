# Ombi APT repo

```bash
curl -sSL https://roxedus.github.io/apt-test/apt/pub.key | sudo apt-key add -
echo "deb https://roxedus.github.io/apt-test/apt focal develop" | tee /etc/apt/sources.list.d/ombi.list
```
