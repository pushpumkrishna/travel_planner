from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from backend_single_agent.config.config import AzureConfig
from backend_single_agent.config.logging_lib import logger
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

class AzureOpenAIModels(AzureConfig):
    def __init__(self):
        """
        Initializes the AzureOpenAIConfig class with a config file.
        """
        super().__init__()

    # def get_azure_embedding_model(self) -> AzureOpenAIEmbeddings:
    #     """
    #     Initializes and returns the Azure embedding model.
    #
    #     :return: OpenAIEmbeddings instance.
    #     """
    #     # Logging.info("Initializing Azure embedding model...")
    #     try:
    #         # azure_config = AzureConfig()
    #         embedding_model = AzureOpenAIEmbeddings(
    #             azure_endpoint=self.get_azure_openai_base,
    #             api_key=self.get_azure_openai_key,
    #             api_version=self.get_azure_openai_api_version,
    #             azure_deployment=self.get_gpt_model_embedding_deployment_name,
    #             model=self.get_gpt_model_embedding,
    #             # chunk_size=1,
    #             # openai_api_type=self.get_azure_openai_api_type,
    #             # api_key=self.get_azure_openai_key,
    #             # azure_deployment=self.get_gpt_model_embedding_deployment_name,
    #         )
    #         logger.info("Azure embedding model initialized.")
    #         return embedding_model
    #     except KeyError as exception:
    #         logger.error(f"Error: Missing key in config file: {exception}")
    #         raise

    # @staticmethod
    def get_azure_model_35(self, temperature: float = 0.7) -> AzureChatOpenAI:
        """
        Initializes and returns the Azure GPT-3.5 model.

        :param temperature: Temperature setting for the model.
        :return: AzureChatOpenAI instance.
        """
        logger.info("Initializing Azure GPT-3.5 model...")
        try:
            model = AzureChatOpenAI(
                azure_endpoint=self.get_azure_openai_base,
                api_key=self.get_azure_openai_key,
                api_version=self.get_azure_openai_api_version,
                azure_deployment=self.get_gpt_model_deployment_name,
                temperature=temperature,
            )
            # Logging.info("Azure GPT-3.5 model initialized.")
            return model
        except KeyError as exception:
            logger.error(f"Error: Missing key in config file: {exception}")
            raise

    # @staticmethod
    def get_azure_model_4(self, temperature: float = 0.0) -> AzureChatOpenAI:
        """
        Initializes and returns the Azure GPT-4 model.

        :return: AzureOpenAI instance.
        """
        logger.info("Initializing Azure GPT-4 model...")
        try:
            # azure_config = AzureConfig()
            model = AzureChatOpenAI(
                azure_endpoint=self.get_azure_openai_base,
                api_key=self.get_azure_openai_key,
                api_version=self.get_azure_openai_api_version,
                azure_deployment=self.get_gpt_model_preview_deployment_name,
                temperature=temperature,
                max_tokens=2000,
            )
            logger.info("Azure GPT-4 model initialized.")
            return model
        except KeyError as exception:
            logger.error(f"Error: Missing key in config file: {exception}")
            raise



    def get_azure_model_4_test(self, temperature: float = 0.0) -> AzureChatOpenAI:
        """
            Initializes and verifies the Azure GPT-4 model.

            :return: AzureChatOpenAI instance.
            """
        logger.info("Initializing Azure GPT-4 model...")
        try:
            model = AzureChatOpenAI(
                azure_endpoint=self.get_azure_openai_base,
                api_key=self.get_azure_openai_key,
                api_version=self.get_azure_openai_api_version,
                azure_deployment=self.get_gpt_model_preview_deployment_name,
                temperature=temperature,
                max_tokens=2000,
            )

            # 🔹 Test call to validate credentials
            logger.info("Testing Azure GPT-4 connection...")
            response = model.invoke([
                HumanMessage(content="Say 'OK' if you are working.")
            ])

            logger.info(f"Azure GPT-4 test response: {response.content}")
            logger.info("Azure GPT-4 model is working correctly.")

            return model

        except Exception as exception:
            logger.error("Azure GPT-4 initialization/test failed.")
            raise


# Example usage:
if __name__ == "__main__":
    try:
        # Initialize configuration and models
        azure_config = AzureOpenAIModels()
        # azure_embedding_model = azure_config.get_azure_embedding_model()
        azure_model_35 = azure_config.get_azure_model_35()
        azure_model_4 = azure_config.get_azure_model_4()
        azure_model_41 = azure_config.get_azure_model_4_test()


        # Proceed with further processing using these models
        print("Models initialized successfully.")
    except Exception as exception_:
        print(f"An exception occurred: {exception_}")
