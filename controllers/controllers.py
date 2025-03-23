from flask import request, jsonify
from app import app
import services.services as services  # Ensure correct import

@app.route('/getStockRanks', methods=['POST'])
def stock_ranks():
    app.logger.info("Entering endpoint '/getStockRanks' route")

    try:
        # Get JSON data from request
        result, err = services.getStockRanks(request.json, request.headers)
        
        if err:
            return jsonify({"status": "error", "message": str(err)}), 400

        response = {
            "status": "success",
            "totalStocks": len(result),
            "stocks": result
        }
        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"status": "error", "message": "Invalid request"}), 400