"""! @brief Pipeline entry point."""
import asyncio
from pipeline.pipeline import IkidoClassifierPipeline
from pipeline.schema.inputs import IkidoClassifierInputs


##
# @file
#
# @brief Pipeline entry point.
if __name__ == '__main__':
    ## Creates an instance of the pipeline
    p = IkidoClassifierPipeline()

    ## This method executes the pipeline, dataset and required params can be loaded here.\n
    # Examples:
    # @code
    # data = {}
    # for file in data_files:
    #     with open(file) as f:
    #         data = load_json(f)
    #
    # output = p.execute(**data)
    # @endcode
    # or
    # @code
    # p.execute(data=mydata)
    # @endcode
    # or
    # @code
    # sig = Signature(uid=1, text=signature, hints=None)
    # output = p.execute(signatures=[sig])
    # @endcode
    # Define data passed through the execute method in the schema/<my-new-project>Inputs.py class, for example:
    # @code
    # class <my-new-project>Inputs(BaseModel):
    #     signatures: List[Signature]
    # @endcode
    # or
    # @code
    # class <my-new-project>Inputs(BaseModel):
    #     data = {}
    # @endcode
    # data = IkidoClassifierInputs(
    #     pdf_datasheet_url='https://app.ikido.tech/api/datasheet/9cd85784796b00d29e76deaefc9f8ad43a9c199b268a953546b6027c572e9c6d0713fd4b62cfaf3cb3c0ac07f477668c088f63562542db5ececb7627258d84e7/KEM_T2005_T491-1093550.pdf',
    #     pdf_datasheet_text=''
    # )
    data = {
        'inputs': [
            {
                'pdf_datasheet_url': 'https://app.ikido.tech/api/datasheet/9cd85784796b00d29e76deaefc9f8ad43a9c199b268a953546b6027c572e9c6d0713fd4b62cfaf3cb3c0ac07f477668c088f63562542db5ececb7627258d84e7/KEM_T2005_T491-1093550.pdf',
                # 'pdf_datasheet_text': ''
            },
            # {
            #     'pdf_datasheet_url': 'https://app.ikido.tech/api/datasheet/726bcdbb59236306c8da366f71c785a019ea92943a6b01ae9c53cee82fcee2f9559d55a0c92ab5f5ef7680fe9a5453ea275317a1765166cf3c4ab107cf8a3244/PYu-AC_51_RoHS_L_9.pdf',
            #     # 'pdf_datasheet_text': ''
            # }
        ]
    }
    output = p.execute(**data)
    print(output)


    # for streaming
    # output = p.execute_stream()
    # async def stream_response():
    #     count = 0
    #     final_text = ''
    #     async for chunk in output:
    #         count += 1
    #         final_text = chunk['text']
    #         print('final_text', final_text)
    #
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(stream_response())
