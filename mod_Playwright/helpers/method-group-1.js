// Version: 1.0
const { url } = require("../constants/urls");

class ApiClient {
  constructor(request) {
    this.api = {};
    this.request = request;

    this.requestMessage = function(method, endpoint) {
      console.log(`[+] ${method} request to ${endpoint}`);
    };
  }
  async getOtomotoOffer() {
    const endpoint = url.otomoto;

    this.requestMessage("GET", endpoint);
  }
}

module.exports = ApiClient;
