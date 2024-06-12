// Version: 1.0
const { url } = require("../constants/endpoints");

class ApiClient {
    constructor(request) {
        this.api = {};
        this.request = request;
    }

    async getOtomotoOffer() {
        const endpoint = ENDPOINTS.otomoto;
        const response = await this.request.get(endpoint);
        return response;
    }
}

module.exports = ApiClient;
