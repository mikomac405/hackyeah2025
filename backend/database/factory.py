"""
Database factory for creating repository instances
"""

import os
from .repository import Repository
from .sqlite_repository import SQLiteRepository


class DatabaseFactory:
    """Factory class for creating database repository instances"""
    
    _instance: Repository = None
    
    @classmethod
    def get_repository(cls, db_type: str = None, **kwargs) -> Repository:
        """
        Get or create a repository instance
        
        Args:
            db_type: Type of database ('sqlite', 'postgres', etc.)
            **kwargs: Additional arguments for repository initialization
            
        Returns:
            Repository instance
        """
        if cls._instance is None:
            cls._instance = cls.create_repository(db_type, **kwargs)
        return cls._instance
    
    @classmethod
    def create_repository(cls, db_type: str = None, **kwargs) -> Repository:
        """
        Create a new repository instance
        
        Args:
            db_type: Type of database ('sqlite', 'postgres', etc.)
            **kwargs: Additional arguments for repository initialization
            
        Returns:
            Repository instance
        """
        # Get db_type from environment or default to sqlite
        if db_type is None:
            db_type = os.environ.get('DB_TYPE', 'sqlite').lower()
        
        if db_type == 'sqlite':
            db_path = kwargs.get('db_path', os.environ.get('DB_PATH', 'pension_simulator.db'))
            return SQLiteRepository(db_path=db_path)
        # Add more database types here as needed
        # elif db_type == 'postgres':
        #     return PostgresRepository(**kwargs)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    @classmethod
    def reset(cls):
        """Reset the singleton instance (useful for testing)"""
        if cls._instance:
            cls._instance.close()
        cls._instance = None


def get_db() -> Repository:
    """
    Convenience function to get the database repository
    
    Returns:
        Repository instance
    """
    return DatabaseFactory.get_repository()
