from elasticsearch import Elasticsearch
import os
from flask import current_app

class ElasticsearchService:
    def __init__(self):
        es_uri = os.getenv("ELASTICSEARCH_URI")
        es_user = os.getenv("ELASTICSEARCH_USER", "elastic") 
        es_password = os.getenv("ELASTICSEARCH_PASSWORD", "")

        self.es = Elasticsearch(
        [es_uri],
        basic_auth=(es_user, es_password),
        verify_certs=False  # For development only
    )
            
    def index_plan(self, plan):
        """Index a plan and its child components in Elasticsearch with proper join field"""
        # Copy plan to avoid modifying the original
        plan_copy = plan.copy()
        
        # Add join relation field to the plan
        plan_copy["relation"] = "plan"
        
        # Index the main plan document
        plan_id = plan_copy["objectId"]
        self.es.index(index="plan_index", id=plan_id, body=plan_copy)
        
        # Index linked services as child documents
        for service in plan.get("linkedPlanServices", []):
            service_copy = service.copy()
            
            # Add join relation field to service with parent reference
            service_copy["relation"] = {
                "name": "service",
                "parent": plan_id
            }
            
            service_id = service_copy["objectId"]
            
            # Index with routing to ensure child is stored with parent
            self.es.index(
                index="plan_index",
                id=service_id,
                routing=plan_id,  # Routing ensures child is stored with parent
                body=service_copy
            )
        
        return True
    
    def update_plan(self, plan_id, plan):
        """Update a plan and its child components with proper join relation"""
        # Add join relation field to the plan
        plan_copy = plan.copy()
        plan_copy["relation"] = "plan"
        
        # Update the main plan
        self.es.index(index="plan_index", id=plan_id, body=plan_copy)
        
        # Update linked services
        for service in plan.get("linkedPlanServices", []):
            service_copy = service.copy()
            service_copy["relation"] = {
                "name": "service",
                "parent": plan_id
            }
            
            service_id = service_copy["objectId"]
            
            # Update with routing
            self.es.index(
                index="plan_index",
                id=service_id,
                routing=plan_id,
                body=service_copy
            )
        
        return True

    def delete_plan(self, plan_id):
        """Delete a plan and its child components"""
        # Delete child services first - using a query
        query = {
            "query": {
                "has_parent": {
                    "parent_type": "plan",
                    "query": {
                        "term": {
                            "objectId": plan_id
                        }
                    }
                }
            }
        }
        
        self.es.delete_by_query(index="plan_index", body=query)
        # Then delete the plan itself
        self.es.delete(index="plan_index", id=plan_id)
        return True
    
    def search_plans(self, query_string):
        """Search for plans in Elasticsearch"""
        query = {
            "query": {
                "query_string": {
                    "query": query_string
                }
            }
        }
        
        results = self.es.search(index="plan_index", body=query)
        return results["hits"]["hits"]

# Initialize Elasticsearch service as a singleton
es_service = ElasticsearchService()