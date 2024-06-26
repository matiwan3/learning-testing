const { url } = require('../../constants/urls');

class DevPage {
  constructor(page) {
    this.page = page;
    this.playwrightLogoText = this.page.locator('#navbar__logo');
  }

  async goto() {
    await this.page.goto(url.playwright);
  }
}

exports.DevPage = DevPage;
