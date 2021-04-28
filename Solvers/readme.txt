SolversInterface has some function you must to implement if you want to use it with sklearn examples:
# get_supported_models: which models do we support? (SVC, Logistic Regression, ..)
# train(X_train, y_train, *args, **kwargs)
    # X_train - X data set to fit with Y train
    # Y_train - Y data set to fit with X train
    # *args - arguments
    # **kwargs - keyword arguments
# load_from_json - convert json to model
# export_to_json - convert model to json