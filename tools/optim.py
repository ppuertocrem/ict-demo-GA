def process_optim(graph_possible, operations_possible, needs, io_cstr_fun, obj_fun):
    """
    Reduce possible energy flows between technology options graph to a choosen 
    technology graph, choosing optimal operation given needs, input/outputs nodes models 
    and objective function. Determine technology design with max values of optimal flows.
    """

    flows, choice = base_optim(graph_possible, operations_possible, needs, io_cstr_fun, obj_fun)

    operation = operations_possible[[v.x for v in choice.values()].index(1)]
    selected_flows = {link: [v.x for v in flows.select(link[0], link[1], operation, '*')] for link in graph_possible}

    graph_choice, design = design_from_raw_optim_results(selected_flows)

    return graph_choice, design, operation


def design_from_raw_optim_results(flows):
    """
    Extract design for technology nodes from optimal selected flows results.
    """
    design = 0
    return design


def base_optim(graph_possible, operations_possible, needs, io_cstr_fun, obj_fun):
    """
    Compute optimal flow optimisation.
    """
    flows, choice = (0, 0)
    return flows, choice
