plan_schema = {
    "type": "object",
    "properties": {
        "planCostShares": {
            "type": "object",
            "properties": {
                "deductible": {"type": "integer"},
                "_org": {"type": "string"},
                "copay": {"type": "integer"},
                "objectId": {"type": "string"},
                "objectType": {"type": "string"}
            },
            "required": ["deductible", "_org", "copay", "objectId", "objectType"]
        },
        "linkedPlanServices": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "linkedService": {
                        "type": "object",
                        "properties": {
                            "_org": {"type": "string"},
                            "objectId": {"type": "string"},
                            "objectType": {"type": "string"},
                            "name": {"type": "string"}
                        },
                        "required": ["_org", "objectId", "objectType", "name"]
                    },
                    "planserviceCostShares": {
                        "type": "object",
                        "properties": {
                            "deductible": {"type": "integer"},
                            "_org": {"type": "string"},
                            "copay": {"type": "integer"},
                            "objectId": {"type": "string"},
                            "objectType": {"type": "string"}
                        },
                        "required": ["deductible", "_org", "copay", "objectId", "objectType"]
                    },
                    "_org": {"type": "string"},
                    "objectId": {"type": "string"},
                    "objectType": {"type": "string"}
                },
                "required": ["linkedService", "planserviceCostShares", "_org", "objectId", "objectType"]
            }
        },
        "_org": {"type": "string"},
        "objectId": {"type": "string"},
        "objectType": {"type": "string"},
        "planType": {"type": "string"},
        "creationDate": {"type": "string", "pattern": "^\d{2}-\d{2}-\d{4}$"}
    },
    "required": ["planCostShares", "linkedPlanServices", "_org", "objectId", "objectType", "planType", "creationDate"]
}
