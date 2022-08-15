from django.http import HttpResponse
from minizinc import Instance, Model, Solver
from django.core.mail import send_mail

def hello(request, name):
    return HttpResponse(f"<h2>Hello {name}</h2>")

def minizinc(request, n):
    # Load n-Queens model from file
    nqueens = Model()
    nqueens.add_string("""
        int: n; % The number of queens.

        array [1..n] of var 1..n: q;

        include "alldifferent.mzn";

        constraint alldifferent(q);
        constraint alldifferent(i in 1..n)(q[i] + i);
        constraint alldifferent(i in 1..n)(q[i] - i);"""
    )
    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup("gecode")
    # Create an Instance of the n-Queens model for Gecode
    instance = Instance(gecode, nqueens)
    # Assign 4 to n
    instance["n"] = int(n)
    result = instance.solve()
    # Output the array q
    return HttpResponse(f'<h2>{result["q"]}</h2>')

def send_me_email(request):
    send_mail('Django', "Toto je zkouska posilani emailu", 'v.kostejn.experimental@gmail.com', ['v.kostejn.vk@gmail.com'], fail_silently=False)
    return HttpResponse("Email was sent")

# if __name__ == '__main__':
#     minizinc(None)